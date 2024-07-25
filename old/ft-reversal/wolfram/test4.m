(* Define the variable and the expression to solve *)
x = Symbol["x"];
expr = Integrate[Sin[x]^2 * Cos[x], x];

(* Query Wolfram Alpha for a step-by-step solution using the actual expression *)
result = WolframAlpha["integrate " <> ToString[Unevaluated[expr], InputForm],
                      {{"IndefiniteIntegral", 2}, "Content"},
                      PodStates -> {"IndefiniteIntegral__Step-by-step solution"}];

(* Convert the result to plain text and print it *)
plainTextResult = TextString[result];
Print[plainTextResult];
