(* Define the expression to solve *)
expr = Integrate[Sin[x]^2 * Cos[x], x];

(* Query Wolfram Alpha for a step-by-step solution using the actual expression *)
result = WolframAlpha["integrate " <> ToString[expr, InputForm], 
                      "Result", 
                      PodStates -> {"Step-by-step solution"}];

(* Print the step-by-step solution *)
Print[result];
