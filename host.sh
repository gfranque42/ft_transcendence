argc=$#
argv=("$@")
declare -i b=1
declare -i a=0

if [ $argc -eq $b ]; then
	if test -e ${argv[$a]}; then
		echo -n "ALLOWED_HOSTS = ['" > .host
		hostname -s | tr -d '\n' >> .host
		echo "', 'localhost']" >> .host
		declare -i i=1
		declare -i n=1
		while [ $i -eq $n ];
		do
			if grep -q "ALLOWED_HOSTS = \['" ${argv[$a]}; then
				head -n -1 ${argv[$a]} > settings.py.tmp ; mv settings.py.tmp ${argv[$a]}
			else
				i=0
			fi
		done
		cat .host >> ${argv[$a]} ; rm .host
	fi
fi