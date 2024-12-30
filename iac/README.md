Fresh aws account, manually create:
1)  **browser**: profile for acccount [non root user]
2)  **browser**: associated policies to root user to allow setting up the backend state buckets 
3)  **CLI**: configure aws cli to work with created profile 
`web aws configure --profile dev`
4) runnng `tf plan` and `tf apply` showed that the profile dev will be used to provision the resources. Further update to permissions required