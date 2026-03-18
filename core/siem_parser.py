import re
from datetime import datetime

class LogParser:
    # Common log patterns
    PATTERNS = {
        'syslog': r'(?P<timestamp>\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(?P<hostname>\S+)\s+(?P<process>[\w\/\.\-]+)(?:\[(?P<pid>\d+)\])?:\s+(?P<message>.*)',
        'auth_failed': r'Failed password for (?P<user>\S+) from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port (?P<port>\d+) ssh2',
        'auth_success': r'Accepted password for (?P<user>\S+) from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) port (?P<port>\d+) ssh2',
        'web_access': r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+\-\s+\-\s+\[(?P<timestamp>.*?)\]\s+"(?P<method>\w+)\s+(?P<path>\S+)\s+.*?"\s+(?P<status>\d+)\s+(?P<size>\d+)'
    }

    @staticmethod
    def parse_line(line, log_type='syslog'):
        pattern = LogParser.PATTERNS.get(log_type)
        if not pattern:
            return None
        
        match = re.search(pattern, line)
        if match:
            data = match.groupdict()
            data['raw'] = line
            data['type'] = log_type
            data['parsed_at'] = datetime.now().isoformat()
            return data
        return None

# Test parser
if __name__ == "__main__":
    test_line = "Mar 18 14:10:05 server sshd[1234]: Failed password for root from 192.168.1.100 port 54321 ssh2"
    parser = LogParser()
    print(parser.parse_line(test_line, 'auth_failed'))
