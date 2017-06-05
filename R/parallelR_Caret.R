# Adapted from caret-parallel-train.R in Caret examples
# to Triton by Simo Tuomisto, 2017

# Original docstring:
# Run multiple caret models in parallel using lapply
# https://github.com/tobigithub/caret-machine-learning
# Tobias Kind (2015)


# Get the number of cores to use from command line or from SLURM_CPUS_PER_TASK
library("optparse")

option_list = list(
  make_option(c("-c", "--cores"), type="integer", default=NULL, 
                help="Number of cpus to use", metavar="integer")); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

if (is.null(opt$cores)) {
  cores <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK"))
  if (is.na(cores)) {
    cores <- 1
  }
} else {
    cores <- opt$cores
}
message("Number of cores used: ",cores)

# -------------------------------------------------------------------------
# FIRST sequential code (not parallel one CPU core):
# ------------------------------------------------------------------------- 


require(caret); data(BloodBrain); set.seed(123)


message('Running Caret training in serial fashion')
system.time(fit1 <- train(bbbDescr, logBBB, "knn"))
fit1

# ------------------------------------------------------------------------- 
# SECOND parallel register 4 cores (no worries if you only have 2)
# train the caret model in parallel 
# -------------------------------------------------------------------------

message('Running Caret training in parallel fashion')
library(doParallel)
cl <- makeCluster(cores)
registerDoParallel(cl) 

require(caret); data(BloodBrain); set.seed(123)

system.time(fit1 <- train(bbbDescr, logBBB, "knn"))
fit1

stopCluster(cl)
registerDoSEQ()

### END
