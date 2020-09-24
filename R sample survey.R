

#SURVEY ANALYSIS: this code will not run because the data file is too big to put onto the Github repo, but I wanted to include some anyway because this election study analysis was an extended project I worked on.


full_anes = read.dta("anes_timeseries_2016_Stata12.dta")

anes_design = svydesign(ids = ~V160202, strata = ~V160201, weights = ~V160102, data = full_anes, nest = T)

anes_srvyr_design <- as_survey(anes_design)


#Plotting two correlated variables as a barplot

blm.party = summarize(group_by(anes_srvyr_design, V161158x), 
                      mean = survey_mean(V162113, na.rm = TRUE))
barplot(height = blm.party$mean[3:9], 
        names.arg = c("Strong Democrat",'Not very strong Democrat',
                      'Independent-Democrat','Independent','Independent-Republican',
                      'Not very strong Republican','Strong Republican'),
        col = colorspace::diverge_hsv(7),
        xlab = 'Political Affiliation', ylab = 'Mean Rating (0-100 scale)', ylim = c(0,100),
        main = "Feelings towards Black Lives Matter")




#Plotting two categoricals as a mosaic plot with shaded standardized residuals

library(gplots)

index = which((full_anes$V161158x != "-8. DK (-8) in V161156 or V161157 (FTF only)" & full_anes$V161158x != "-9. RF (-9) in V161155 (FTF only)/-9 in V161156 or V161157 ") & (full_anes$V161310x != "-2. Missing"))

race.party = as.matrix(table(full_anes$V161310x[index], full_anes$V161158x[index]))
race.party = race.party[apply(race.party[,-1], 1, function(x) !all(x==0)),]
race.party = race.party[, -(colSums(abs(race.party)) == 0)]
race.party = race.party[, -(colSums(abs(race.party)) == 0)]
race.party = race.party[, -(colSums(abs(race.party)) == 0)]

dimnames(race.party)[[1]] <- c("White", "Black", "Asian", "Native American", "Hispanic", "Other")
dimnames(race.party)[[2]] <- c("Strong Democrat",'Not very strong Democrat',
                               'Independent-Democrat','Independent','Independent-Republican',
                               'Not very strong Republican','Strong Republican')


mosaicplot(race.party, las = 2, main = "Political Affiliation by Race", 
           color = colorspace::diverge_hcl(7), type = "pearson", shade = T)





# Using Tukey HSD test and anova to determine differences in feelings towards poor people:

poor.party = summarize(group_by(anes_srvyr_design, V161158x), 
                       mean = survey_mean(V162099, na.rm = TRUE))
barplot(height = poor.party$mean[3:9], 
        names.arg = c("Strong Democrat",'Not very strong Democrat',
                      'Independent-Democrat','Independent','Independent-Republican',
                      'Not very strong Republican','Strong Republican'),
        col = colorspace::diverge_hcl(7),
        xlab = 'Political Affiliation', ylab = 'Mean Rating (0-100 scale)', ylim = c(0,100),
        main = "Feelings towards Poor People")    

index = which(full_anes$V161158x != "-8. DK (-8) in V161156 or V161157 (FTF only)" & 
                full_anes$V161158x != "-9. RF (-9) in V161155 (FTF only)/-9 in V161156 or V161157 " & 
                (full_anes$V162099 <= 100))    
poor.party.aov = aov(V162099[index] ~ V161158x[index], data = full_anes) #, weights = full_anes$V160102[index])


summary.lm(poor.party.aov)
TukeyHSD(poor.party.aov)