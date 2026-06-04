import pandas as pd
import re

# ─────────────────────────────────────────────────────────────────────────────
# WhatsApp Chat Preprocessor — Flexible Multi-Format Parser
#
# Handles all known WhatsApp export formats:
#   Android 24h  : 06/11/23, 22:22 - Name: Message
#   Android 12h  : 6/11/23, 10:22 PM - Name: Message
#   iOS bracket  : [06/11/23, 22:22:45] Name: Message
#   Dot separator: 06.11.23, 22:22 - Name: Message
#   Multi-line messages (continuation lines without a timestamp)
#   Group notifications (no colon in username part)
# ─────────────────────────────────────────────────────────────────────────────

# Each entry: (non-capturing-split-regex, date-capture-regex, parse-hint)
# Split regex: used to split the whole text on message boundaries (no groups → no extra splits)
# Date regex: used to extract and parse the date portion
_FORMATS = [
    {
        'name': 'android_24h',
        # 06/11/23, 22:22 -   OR   6.11.2023, 22:22 -
        'split': re.compile(r'\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4},\s*\d{1,2}:\d{2}\s*-\s*'),
        'extract': re.compile(r'^(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4}),\s*(\d{1,2}):(\d{2})\s*-\s*$'),
        'has_ampm': False,
        'has_secs': False,
        'bracket': False,
    },
    {
        'name': 'android_12h',
        # 06/11/23, 10:22 AM -   OR   6/11/23, 10:22 PM -
        'split': re.compile(r'\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4},\s*\d{1,2}:\d{2}\s*[AaPp][Mm]\s*-\s*'),
        'extract': re.compile(r'^(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4}),\s*(\d{1,2}):(\d{2})\s*([AaPp][Mm])\s*-\s*$'),
        'has_ampm': True,
        'has_secs': False,
        'bracket': False,
    },
    {
        'name': 'ios_bracket_24h_sec',
        # [06/11/23, 22:22:45]
        'split': re.compile(r'\[\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4},\s*\d{1,2}:\d{2}:\d{2}\]\s*'),
        'extract': re.compile(r'^\[(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4}),\s*(\d{1,2}):(\d{2}):(\d{2})\]\s*$'),
        'has_ampm': False,
        'has_secs': True,
        'bracket': True,
    },
    {
        'name': 'ios_bracket_12h_sec',
        # [6/11/23, 10:22:45 AM]
        'split': re.compile(r'\[\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4},\s*\d{1,2}:\d{2}:\d{2}\s*[AaPp][Mm]\]\s*'),
        'extract': re.compile(r'^\[(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4}),\s*(\d{1,2}):(\d{2}):(\d{2})\s*([AaPp][Mm])\]\s*$'),
        'has_ampm': True,
        'has_secs': True,
        'bracket': True,
    },
    {
        'name': 'ios_bracket_24h',
        # [06/11/23, 22:22]
        'split': re.compile(r'\[\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4},\s*\d{1,2}:\d{2}\]\s*'),
        'extract': re.compile(r'^\[(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4}),\s*(\d{1,2}):(\d{2})\]\s*$'),
        'has_ampm': False,
        'has_secs': False,
        'bracket': True,
    },
    {
        'name': 'ios_bracket_12h',
        # [6/11/23, 10:22 AM]
        'split': re.compile(r'\[\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4},\s*\d{1,2}:\d{2}\s*[AaPp][Mm]\]\s*'),
        'extract': re.compile(r'^\[(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4}),\s*(\d{1,2}):(\d{2})\s*([AaPp][Mm])\]\s*$'),
        'has_ampm': True,
        'has_secs': False,
        'bracket': True,
    },
]


def _parse_ts(ts_str: str, fmt: dict, date_order: str = 'DMY') -> pd.Timestamp:
    """Parse a single timestamp string using the given format dict and date order."""
    ts_str = ts_str.strip()
    m = fmt['extract'].match(ts_str)
    if not m:
        return pd.NaT

    g = m.groups()
    if date_order == 'MDY':
        month, day, year = int(g[0]), int(g[1]), int(g[2])
    else:
        day, month, year = int(g[0]), int(g[1]), int(g[2])
        
    hour, minute = int(g[3]), int(g[4])
    sec = 0

    if year < 100:
        year += 2000

    if fmt['has_secs'] and fmt['has_ampm']:
        sec = int(g[5])
        ampm = g[6].upper()
    elif fmt['has_secs']:
        sec = int(g[5])
        ampm = None
    elif fmt['has_ampm']:
        ampm = g[5].upper()
    else:
        ampm = None

    if ampm == 'PM' and hour != 12:
        hour += 12
    elif ampm == 'AM' and hour == 12:
        hour = 0

    try:
        return pd.Timestamp(year=year, month=month, day=day,
                            hour=hour, minute=minute, second=sec)
    except Exception:
        # Swap day/month in case of format anomaly
        try:
            return pd.Timestamp(year=year, month=day, day=month,
                                hour=hour, minute=minute, second=sec)
        except Exception:
            return pd.NaT


def _detect_format(text: str) -> dict:
    """Return the format dict whose split regex matches the most lines (≥ 5)."""
    best_fmt = None
    best_count = 0
    for fmt in _FORMATS:
        count = len(fmt['split'].findall(text))
        if count > best_count:
            best_count = count
            best_fmt = fmt
    if best_count < 5:
        return None
    return best_fmt


def preprocess(data: str) -> pd.DataFrame:
    """
    Parse a WhatsApp chat export text into a structured DataFrame.

    Returns a DataFrame with columns:
        date, users, message, year, month_num, specific_date,
        day_name, month, day, hour, minute, period
    """
    # Normalize line endings and narrow no-break spaces
    data = data.replace('\r\n', '\n').replace('\r', '\n')
    data = data.replace('\u202f', ' ').replace('\u2013', '-')

    # ── Detect format ────────────────────────────────────────────────────────
    fmt = _detect_format(data)
    if fmt is None:
        raise ValueError(
            "Could not detect a known WhatsApp date format in this file.\n"
            "Please export the chat from WhatsApp → Open Chat → ⋮ → More → Export Chat → Without Media."
        )

    # ── Find all timestamp match positions ───────────────────────────────────
    # We scan line by line: lines that START with a timestamp begin a new message;
    # other lines are continuation of the previous message.
    lines = data.split('\n')

    timestamps_raw = []
    message_bodies = []
    current_ts = None
    current_body_lines = []

    for line in lines:
        m = fmt['split'].match(line)
        if m:
            # Save the previous message
            if current_ts is not None:
                message_bodies.append('\n'.join(current_body_lines).strip())
            # Start new message
            ts_str = m.group(0)                 # the matched timestamp prefix
            rest = line[m.end():]               # everything after the timestamp
            timestamps_raw.append(ts_str.strip())
            current_ts = ts_str
            current_body_lines = [rest]
        else:
            # Continuation line (multi-line message)
            if current_ts is not None:
                current_body_lines.append(line)

    # Don't forget the last message
    if current_ts is not None:
        message_bodies.append('\n'.join(current_body_lines).strip())

    # ── Detect Date Order Heuristic (DMY vs MDY) ─────────────────────────────
    # Scan all found raw timestamps to check if we find a number > 12 in day/month position
    date_order = 'DMY'
    for ts in timestamps_raw:
        m = fmt['extract'].match(ts)
        if m:
            g = m.groups()
            first = int(g[0])
            second = int(g[1])
            if first > 12:
                date_order = 'DMY'
                break
            if second > 12:
                date_order = 'MDY'
                break

    # ── Parse timestamps ─────────────────────────────────────────────────────
    dates = [_parse_ts(ts, fmt, date_order) for ts in timestamps_raw]

    # ── Split each message body into user + message text ─────────────────────
    users = []
    messages = []
    for body in message_bodies:
        # "Username: message" — username can have spaces/parens/numbers but not newlines
        match = re.match(r'^([^:\n]{1,80}):\s(.+)$', body, re.DOTALL)
        if match:
            users.append(match.group(1).strip())
            messages.append(match.group(2).strip())
        else:
            users.append('group_notification')
            messages.append(body.strip())

    # ── Build DataFrame ──────────────────────────────────────────────────────
    df = pd.DataFrame({'date': dates, 'users': users, 'message': messages})
    df = df[df['date'].notna()].reset_index(drop=True)

    # Filter out future dates (messages beyond the current system date/time)
    df = df[df['date'] <= pd.Timestamp.now()].reset_index(drop=True)

    if df.empty:
        raise ValueError("All timestamps failed to parse. The file might be corrupted or in an unsupported locale.")

    # ── Time feature columns ─────────────────────────────────────────────────
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['specific_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['period'] = df['hour'].apply(lambda h: f"{h}-00" if h == 23 else f"{h}-{h+1}")

    return df
