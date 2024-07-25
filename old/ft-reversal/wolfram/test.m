(* Define the function *)
f[x_] := Sin[x] * Log[x];

(* Compute the derivative *)
df = D[f[x], x];

(* Print the derivative *)
Print[df];
