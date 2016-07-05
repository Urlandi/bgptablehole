@ECHO OFF

echo /32,/31,/30,/29,/28,/27,/26,/25,/24,/23,/22,/21,/20,/19,/18,/17,/16,/15,/14,/13,/12,/10,/9,/8,/7,/6,/5,/4,/3,/2,/1

CALL :PREFIX_COUNT %1_f.log
CALL :PREFIX_COUNT %1_f1.log
CALL :PREFIX_COUNT %1_f2.log

CALL :PREFIX_COUNT %1_sf.log
CALL :PREFIX_COUNT %1_sf1.log
CALL :PREFIX_COUNT %1_sf2.log

echo.

echo ASN_SRC, ASN_SUM

CALL :ASN_COUNT %1

echo.

echo Total,ASN_SRC,ASN_UPSTREAM,Total_SUM,ASN_SUM,UPSTREAM_SUM

for /l %%i in (1,1,223) DO CALL :PREFIX24_COUNT %%i %1

GOTO STOP

:PREFIX_COUNT
FOR /F "usebackq" %%a IN (`grep -E "/32$|/32[\^, ]" %1 ^| wc -l`) DO (
 set r32=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/31$|/31[\^, ]" %1 ^| wc -l`) DO (
 set r31=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/30$|/30[\^, ]" %1 ^| wc -l`) DO (
 set r30=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/29$|/29[\^, ]" %1 ^| wc -l`) DO (
 set r29=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/28$|/28[\^, ]" %1 ^| wc -l`) DO (
 set r28=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/27$|/27[\^, ]" %1 ^| wc -l`) DO (
 set r27=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/26$|/26[\^, ]" %1 ^| wc -l`) DO (
 set r26=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/25$|/25[\^, ]" %1 ^| wc -l`) DO (
 set r25=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/24$|/24[\^, ]" %1 ^| wc -l`) DO (
 set r24=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/23$|/23[\^, ]" %1 ^| wc -l`) DO (
 set r23=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/22$|/22[\^, ]" %1 ^| wc -l`) DO (
 set r22=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/21$|/21[\^, ]" %1 ^| wc -l`) DO (
 set r21=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/20$|/20[\^, ]" %1 ^| wc -l`) DO (
 set r20=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/19$|/19[\^, ]" %1 ^| wc -l`) DO (
 set r19=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/18$|/18[\^, ]" %1 ^| wc -l`) DO (
 set r18=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/17$|/17[\^, ]" %1 ^| wc -l`) DO (
 set r17=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/16$|/16[\^, ]" %1 ^| wc -l`) DO (
 set r16=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/15$|/15[\^, ]" %1 ^| wc -l`) DO (
 set r15=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/14$|/14[\^, ]" %1 ^| wc -l`) DO (
 set r14=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/13$|/13[\^, ]" %1 ^| wc -l`) DO (
 set r13=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/12$|/12[\^, ]" %1 ^| wc -l`) DO (
 set r12=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/11$|/11[\^, ]" %1 ^| wc -l`) DO (
 set r11=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/10$|/10[\^, ]" %1 ^| wc -l`) DO (
 set r10=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/9$|/9[\^, ]" %1 ^| wc -l`) DO (
 set r9=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/8$|/8[\^, ]" %1 ^| wc -l`) DO (
 set r8=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/7$|/7[\^, ]" %1 ^| wc -l`) DO (
 set r7=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/6$|/6[\^, ]" %1 ^| wc -l`) DO (
 set r6=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/5$|/5[\^, ]" %1 ^| wc -l`) DO (
 set r5=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/4$|/4[\^, ]" %1 ^| wc -l`) DO (
 set r4=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/3$|/3[\^, ]" %1 ^| wc -l`) DO (
 set r3=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/2$|/2[\^, ]" %1 ^| wc -l`) DO (
 set r2=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "/1$|/1[\^, ]" %1 ^| wc -l`) DO (
 set r1=%%a
)
echo %r32%,%r31%,%r30%,%r29%,%r28%,%r27%,%r26%,%r25%,%r24%,%r23%,%r22%,%r21%,%r20%,%r19%,%r18%,%r17%,%r16%,%r15%,%r14%,%r13%,%r12%,%r10%,%r9%,%r8%,%r7%,%r6%,%r5%,%r4%,%r3%,%r2%,%r1%

GOTO STOP

:ASN_COUNT

FOR /F "usebackq" %%a IN (`cut -f 2 -d '^,' %1_f1.log  ^| uniq ^| wc -l`) DO (
 set asn_src=%%a
)

FOR /F "usebackq" %%a IN (`cut -f 2 -d '^,' %1_sf1.log  ^| uniq ^| wc -l`) DO (
 set asn_sum=%%a
)

echo %asn_src%, %asn_sum%

GOTO STOP

:PREFIX24_COUNT

FOR /F "usebackq" %%a IN (`grep -E "^%1\..*/24$|^%1\..*/24[\^, ]" %2_f.log ^| wc -l`) DO (
 set rf=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "^%1\..*/24$|^%1\..*/24[\^, ]" %2_f1.log ^| wc -l`) DO (
 set rf1=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "^%1\..*/24$|^%1\..*/24[\^, ]" %2_f2.log ^| wc -l`) DO (
 set rf2=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "^%1\..*/24$|^%1\..*/24[\^, ]" %2_sf.log ^| wc -l`) DO (
 set rsf=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "^%1\..*/24$|^%1\..*/24[\^, ]" %2_sf1.log ^| wc -l`) DO (
 set rsf1=%%a
)
FOR /F "usebackq" %%a IN (`grep -E "^%1\..*/24$|^%1\..*/24[\^, ]" %2_sf2.log ^| wc -l`) DO (
 set rsf2=%%a
)

echo %1/24,%rf%,%rf1%,%rf2%,%rsf%,%rsf1%,%rsf2%

GOTO STOP



:STOP