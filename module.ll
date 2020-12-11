; ModuleID = ""
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"func"(i32 %"p1", i32 %"p2") 
{
entry:
  %"r" = alloca i32, align 4
  %"summ" = add i32 %"p1", %"p2"
  store i32 %"summ", i32* %"r"
  %"ret_temp" = load i32, i32* %"r", align 4
  ret i32 %"ret_temp"
}

define i32 @"main"() 
{
entry:
  %"x" = alloca i32, align 4
  %".2" = call i32 @"func"(i32 1, i32 2)
  store i32 %".2", i32* %"x"
  %"ret_temp" = load i32, i32* %"x", align 4
  ret i32 %"ret_temp"
}
