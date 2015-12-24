# testthat.R -- automated test cases 
#
# MS 
# Created: Feb 8, 2015

#require("testthat")
require("Ckmeans.1d.dp")

inputFile <- "daily_ranking_pre.csv"
outputFile <- "grouped_result.csv"

con <- file(inputFile, open = "r")
while (length(oneLine <- readLines(con, n = 1)) > 0) {
	myLine <- unlist((strsplit(oneLine, ",")))
	record <- c()
	index <- 0
	r_date <- ""
	for(i in myLine){
		if(index == 0){
			r_date = i
		}
		
		if(index > 0){
			record <- c(record, i)
		}
		
		index <- index + 1
	}
	
	result <- Ckmeans.1d.dp(record, 4)
	
	to_write <- c(r_date)
	for(i in result['cluster']['cluster']){
		to_write <- c(to_write, i)
	}
	write(c(to_write), file = outputFile, ncolumns=length(to_write), append = TRUE, sep = ",")
}
close(con)