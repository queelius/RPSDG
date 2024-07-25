(* Define the variable and the expression to solve *)
x = Symbol["x"];
expr = Defer[Integrate[Sin[x]^2 * Cos[x], x]];  // Already specifies the integration

(* Convert the expression to a string *)
exprString = ToString[expr];

Print["Original Expression"];
Print[exprString];
exprString = "integrate sin(x)^2 cos(x) dx";

(* Query Wolfram Alpha for a step-by-step solution using the actual expression *)
result = WolframAlpha[exprString,
                      "Result", 
                      PodStates -> {"Step-by-step solution"}];

(* Convert the result to plain text and print it *)
plainTextResult = ExportString[result, "Text"];

Print["Solution"];
Print[plainTextResult];

Print["Solution alt"];
Print[result];
