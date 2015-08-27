#!/bin/sh

[[ -f whitelist_parsed.txt ]] && rm whitelist_parsed.txt -v

function parse_whois {
	AS=$1
	echo "Parsing ip lists from $AS"
	VARIABLE=`whois -h whois.radb.net -- "-i origin $AS" | grep route: | awk '{print $2}'` 
	echo $VARIABLE >> whitelist_parsed.txt
}

# google
AS="AS45566 AS43515 AS41264 AS36987 AS36492 AS36385 AS36384 AS36040 AS36039 AS22859 AS22577 AS15169"
for i in $AS; do parse_whois $i; done

# yahoo
AS="AS7280 AS7233 AS58721 AS58720 AS58525 AS5779 AS55898 AS55517 AS55418 AS55417 AS55416 AS4694 AS4681 AS45915 AS45863 AS45502 AS45501 AS43428 AS42173 AS40986 AS393245 AS38689 AS38072 AS38045 AS36752 AS36647 AS36646 AS36229 AS36129 AS36088 AS34082 AS34010 AS32116 AS28122 AS26101 AS26085 AS2521 AS24572 AS24506 AS24376 AS24296 AS24236 AS24018 AS23816 AS23663 AS22565 AS18140 AS17110 AS15896 AS15635 AS14678 AS14196 AS131898 AS10880 AS10310 AS10157"
for i in $AS; do parse_whois $i; done

# yandex
AS="AS43247 AS13238"
for i in $AS; do parse_whois $i; done

# facebook AS
parse_whois AS32934

# linkedin
AS="AS40793 AS14413 AS20049"
for i in $AS; do parse_whois $i; done

# Twitter
AS="AS54888 AS35995 AS13414"
for i in $AS; do parse_whois $i; done

# pinterest
parse_whois AS53620

# odnoklassniki
parse_whois AS61119
parse_whois AS49988

# vkontakte
AS="AS47542 AS47541 AS28709"
for i in $AS; do parse_whois $i; done

# mail.ru
AS="AS60863 AS51286 AS47764 AS21051"
for i in $AS; do parse_whois $i; done

# bing microsoft
AS="AS8075 AS8074 AS8073 AS8072 AS8071 AS8070 AS8069 AS8068 AS6584 AS63314 AS6291 AS6194 AS6182 AS5761 AS40066 AS36006 AS3598 AS32476 AS30575 AS30135 AS26222 AS25796 AS23468 AS20046 AS14719 AS13811 AS13399 AS12076"
for i in $AS; do parse_whois $i; done

# resort stored data
cat whitelist_parsed.txt | xargs -n1 | xargs -I{} echo {}\; | sort | uniq > whitelist_parsed.txt.tmp
mv whitelist_parsed.txt.tmp whitelist_parsed.txt -v

# concat with whitelist_ips.custom.txt
cat whitelist_parsed.txt whitelist_ips.custom.txt > whitelist_ips.txt