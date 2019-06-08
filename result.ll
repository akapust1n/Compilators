; ModuleID = "generated"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define i64 @"main"() 
{
entry:
  %"n" = alloca i64
  %"i" = alloca i64
  %"j" = alloca i64
  store i64 5, i64* %"n"
  %"a[5]" = alloca i64
  %"a[0]" = alloca i64
  %"a[1]" = alloca i64
  %"a[2]" = alloca i64
  %"a[3]" = alloca i64
  %"a[4]" = alloca i64
  store i64 1, i64* %"a[0]"
  store i64 2, i64* %"a[1]"
  store i64 3, i64* %"a[2]"
  store i64 4, i64* %"a[3]"
  store i64 6, i64* %"a[4]"
  store i64 0, i64* %"i"
  br label %"entry.forcondition"
entry.forcondition:
  %".12" = load i64, i64* %"i"
  %".13" = load i64, i64* %"n"
  %".14" = icmp slt i64 %".12", %".13"
  %".15" = zext i1 %".14" to i64
  %".16" = sub i64 %".15", 1
  %".17" = load i64, i64* %"i"
  %".18" = load i64, i64* %"n"
  %".19" = icmp slt i64 %".17", %".18"
  %".20" = zext i1 %".19" to i64
  %".21" = sub i64 %".20", 1
  %"forcond" = icmp ne i64 %".21", 0
  br i1 %"forcond", label %"entry.for", label %"entry.endfor"
entry.forincrement:
  %".22" = load i64, i64* %"i"
  %".23" = add i64 %".22", 1
  store i64 %".23", i64* %"i"
  br label %"entry.forcondition"
entry.for:
  store i64 0, i64* %"j"
  br label %"entry.for.forcondition"
  br label %"entry.forincrement"
entry.endfor:
  ret i64 0
entry.for.forcondition:
  %".29" = load i64, i64* %"j"
  %".30" = load i64, i64* %"n"
  %".31" = icmp slt i64 %".29", %".30"
  %".32" = zext i1 %".31" to i64
  %".33" = load i64, i64* %"i"
  %".34" = sub i64 %".33", 1
  %".35" = sub i64 %".32", %".34"
  %".36" = load i64, i64* %"j"
  %".37" = load i64, i64* %"n"
  %".38" = icmp slt i64 %".36", %".37"
  %".39" = zext i1 %".38" to i64
  %".40" = load i64, i64* %"i"
  %".41" = sub i64 %".40", 1
  %".42" = sub i64 %".39", %".41"
  %"forcond.1" = icmp ne i64 %".42", 0
  br i1 %"forcond", label %"entry.for.for", label %"entry.for.endfor"
entry.for.forincrement:
  %".43" = load i64, i64* %"j"
  %".44" = add i64 %".43", 1
  store i64 %".44", i64* %"j"
  br label %"entry.for.forcondition"
entry.for.for:
  %"j1" = alloca i64
  %".46" = load i64, i64* %"j"
  %".47" = add i64 %".46", 1
  store i64 %".47", i64* %"j1"
  %".49" = load i64, i64* %"a[0]"
  %".50" = load i64, i64* %"a[1]"
  %".51" = icmp sgt i64 %".49", %".50"
  %".52" = zext i1 %".51" to i64
  %".53" = load i64, i64* %"a[0]"
  %".54" = load i64, i64* %"a[1]"
  %".55" = icmp sgt i64 %".53", %".54"
  %".56" = zext i1 %".55" to i64
  %".57" = icmp ne i64 %".56", 0
  br i1 %".57", label %"entry.for.for.if", label %"entry.for.for.endif"
  br label %"entry.for.forincrement"
entry.for.endfor:
  br label %"entry.endfor"
entry.for.for.if:
  %"tmp" = alloca i64
  %".59" = load i64, i64* %"a[0]"
  store i64 %".59", i64* %"tmp"
  %".61" = load i64, i64* %"a[1]"
  store i64 %".61", i64* %"a[0]"
  %".63" = load i64, i64* %"tmp"
  store i64 %".63", i64* %"a[1]"
  br label %"entry.for.for.endif"
entry.for.for.endif:
  br label %"entry.for.endfor"
}
