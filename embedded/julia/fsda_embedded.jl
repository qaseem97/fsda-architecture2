using PyCall

gateway_path = joinpath(pwd(), "src", "gateways")
pushfirst!(PyVector(pyimport("sys")."path"), gateway_path)

fsda_module = pyimport("fsda_gateway")
fsda = fsda_module.FSDA()

result = fsda.run("zscoreFS", [1.0 2.0 3.0; 4.0 5.0 6.0; 7.0 8.0 9.0])
println(result)