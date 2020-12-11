; ModuleID = ""
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"soma"(i32 %"a", i32 %"b") 
{
entry:
  %"c" = alloca i32, align 4
  %"summ" = add i32 %"a", %"b"
  store i32 %"summ", i32* %"c"
  %"ret_temp" = load i32, i32* %"c", align 4
  ret i32 %"ret_temp"
}

define i32 @"main"() 
{
entry:
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %".2" = call i32 @"leiaInteiro"()
  store i32 %".2", i32* %"a"
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"b"
  %".6" = load i32, i32* %"a"
  %".7" = load i32, i32* %"b"
  %".8" = call i32 @"soma"(i32 %".6", i32 %".7")
  store i32 %".8", i32* %"c"
  %"write_var" = load i32, i32* %"c", align 4
  call void @"escrevaInteiro"(i32 %"write_var")
  ret i32 0
}
