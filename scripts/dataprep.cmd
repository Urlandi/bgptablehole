cat %1 | tr -s ' ' | cut -f 2,7- -d ' ' | grep -o ".*[0-9]" | sed -r -e "s/0.0.0.0\/0/0.0.0.0\/8/" -e "s/([0-9]+)( \1)+$/\1/" | tee %2.log | sed -r -e "s/^([0-9\.\/]+) (.*)$/\2 \1/" > %2_r.log

start cmd /c " grep -oE "[0-9]+ [\./0-9]+$" %2_r.log | c:\cygwin\bin\sort.exe -n -s -k1,1 | uniq | sed -r -e "s/^(.*) ([0-9\.\/]+)$/\2, \1/" > %2_f1.log"

start cmd /c "cut -f 1 -d ' ' %2.log | uniq > %2_f.log"

start cmd /c "grep -oE "[0-9]+ [0-9]+ [\.\/0-9]+$" %2_r.log | c:\cygwin\bin\sort.exe -n -s -k1,1 -k2,2 | uniq | sed -r -e "s/^(.*) ([0-9\.\/]+)$/\2, \1/" > %2_f2.log"
