#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import re
from utils import *

SUSPICIOUS_REQUEST_PATTERN = (
    ("potential sql injection", r"information_schema|sysdatabases|sysusers|floor\(rand\(|ORDER BY \d+|\bUNION\s+(ALL\s+)?SELECT\b|\b(UPDATEXML|EXTRACTVALUE)\(|\bCASE[^\w]+WHEN.*THEN\b|\bWAITFOR[^\w]+DELAY\b|\bCONVERT\(|VARCHAR\(|\bCOUNT\(\*\)|\b(pg_)?sleep\(|\bSELECT\b.*\bFROM\b.*\b(WHERE|GROUP|ORDER)\b|\bSELECT \w+ FROM \w+|\b(AND|OR|SELECT)\b.*/\*.*\*/|/\*.*\*/.*\b(AND|OR|SELECT)\b|\b(AND|OR)[^\w]+\d+['\") ]?[=><]['\"( ]?\d+|ODBC;DRIVER|\bINTO\s+(OUT|DUMP)FILE"),
    ("potential xml injection", r"/text\(\)='"),
    ("potential php injection", r"<\?php"),
    ("potential ldap injection", r"\(\|\(\w+=\*"),
    ("potential xss injection", r"<script.*?>|\balert\(|(alert|confirm|prompt)\((\d+|document\.|response\.write\(|[^\w]*XSS)|on(mouseover|error|focus)=[^&;\n]+\("),
    ("potential xxe injection", r"\[<!ENTITY"),
    ("potential data leakage", r"im[es]i=\d{15}|(mac|sid)=([0-9a-f]{2}:){5}[0-9a-f]{2}|sim=\d{20}|([a-z0-9_.+-]+@[a-z0-9-.]+\.[a-z]+\b.{0,100}){4}"),
    ("config file access", r"\.ht(access|passwd)|\bwp-config\.php"),
    ("potential remote code execution", r"\$_(REQUEST|GET|POST)\[|xp_cmdshell|shell_exec|\bping(\.exe)? -[nc] \d+|timeout(\.exe)? /T|wget http|curl -O|sh /tmp/|cmd\.exe|/bin/(ba)?sh\b|2>&1|\b(cat|ls) /|chmod [0-7]{3,4}\b|chmod +x\b|nc -l -p \d+|>\s*/dev/null|-d (allow_url_include|safe_mode|auto_prepend_file)|\$\{IFS\}"),
    ("potential directory traversal", r"(\.{2,}[/\\]+){3,}|/etc/(passwd|shadow|issue|hostname)|[/\\](boot|system|win)\.ini|[/\\]system32\b|%SYSTEMROOT%"),
    ("potential web scan", r"(acunetix|injected_by)_wvs_|SomeCustomInjectedHeader|some_inexistent_file_with_long_name|testasp\.vulnweb\.com/t/fit\.txt|www\.acunetix\.tst|\.bxss\.me|thishouldnotexistandhopefullyitwillnot|OWASP%\d+ZAP|chr\(122\)\.chr\(97\)\.chr\(112\)|Vega-Inject|VEGA123|vega\.invalid|PUT-putfile|w00tw00t|muieblackcat"),
)

'''("potential dns changer", r"\b(staticPriDns|staticSecDns|staticThiDns|PriDnsv6|SecDnsv6|ThiDnsv6|staticPriDnsv6|staticSecDnsv6|staticThiDnsv6|pppoePriDns|pppoeSecDns|wan_dns1|wan_dns2|dnsPrimary|dnsSecondary|dnsDynamic|dnsRefresh|DNS_FST|DNS_SND|dhcpPriDns|dhcpSecDns|dnsserver|dnsserver1|dnsserver2|dns_server_ip_1|dns_server_ip_2|dns_server_ip_3|dns_server_ip_4|dns1|dns2|dns3|dns4|dns1_1|dns1_2|dns1_3|dns1_4|dns2_1|dns2_2|dns2_3|dns2_4|wan_dns_x|wan_dns1_x|wan_dns2_x|wan_dns3_x|wan_dns4_x|dns_status|p_DNS|a_DNS|uiViewDns1Mark|uiViewDns2Mark|uiViewDNSRelay|is_router_as_dns|Enable_DNSFollowing|domainserverip|DSEN|DNSEN|dnsmode|dns%5Bserver1%5D|dns%5Bserver2%5D)=")'''



class Filter_module():
	
	def __init__(self, data):
		self.data = data
		#self.logger = Logger(__name__).get_log()
		self.event_logger = event_Logger(__name__).get_event_log()
		self.logger = Logger(__name__).get_log()

	def match(self):
		interfaces = ["/getDataSlice", "/getUsers", "/sendRTMsg", "/getRTMsg", "/getRTMsgLog", "/sendApproval", "/getApprovalById", "/getApproval", "/dealApproval", "/hasNews", "/getNews", "/keyExchange", "/fileAction", "/uploadFile", "/fileInfo" ,"/downloadFile", "/register", "/getVCode", "/userInfo", "/updateUsrInfo", "/login", "/sendApproval", "/getInform"]
		if "command" in self.data:
			if self.data["command"] in interfaces:
				for discription, pattern in  SUSPICIOUS_REQUEST_PATTERN:
					if re.search(pattern, repr(self.data["message"]), re.I):
						#print "=======test======"
						#print pattern
						self.data["danger"] = discription
						self.logger.critical("detect some attack event: "+discription)
						self.event_logger.critical("detect some attack event: "+discription)
						break
			else:
				self.data["danger"] = "request not in the interfaces"
				self.logger.critical("request may be evil")
				self.event_logger.critical("request may be evil")
		return self.data
