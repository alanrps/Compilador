; ModuleID = "module.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare void @"escrevaInteiro"(i32 %".1") 

declare void @"escrevaFlutuante"(float %".1") 

declare i32 @"leiaInteiro"() 

declare float @"leiaFlutuante"() 

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
  %"i" = alloca i32, align 4
  store i32 0, i32* %"i"
  br label %"repita"
repita:
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"a"
  %".6" = call i32 @"leiaInteiro"()
  store i32 %".6", i32* %"b"
  %".8" = load i32, i32* %"a"
  %".9" = load i32, i32* %"b"
  %".10" = call i32 @"soma"(i32 %".8", i32 %".9")
  store i32 %".10", i32* %"c"
  %"write_var" = load i32, i32* %"c", align 4
  call void @"escrevaInteiro"(i32 %"write_var")
  %".13" = load i32, i32* %"i"
  %"summ" = add i32 %".13", 1
  store i32 %"summ", i32* %"i"
  br label %"ate"
ate:
  %"aux_1" = load i32, i32* %"i", align 4
  %"comp" = icmp eq i32 %"aux_1", 5
  br i1 %"comp", label %"repita_fim", label %"repita"
repita_fim:
  ret i32 0
}
