library(reticulate)

use_python("./venv/Scripts/python.exe", required = TRUE)
source_python("./src/gateways/fsda_gateway.py")

fsda <- FSDA()

data <- matrix(c(1,2,3,4,5,6,7,8,9), nrow=3, byrow=TRUE)
result <- fsda$run("zscoreFS", data)
print(result)