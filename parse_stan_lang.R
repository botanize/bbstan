library(jsonlite)
setwd('~/Documents/Science/Projects/MetroTransit/bbstan')
stan_lang = read_json('stan_lang.json')

# keywords:
keywords = c('blocks', 'constants')
ops = sort(unique(names(stan_lang$functions[sapply(stan_lang$functions, function(x) !isTRUE(x$deprecated) & isTRUE(x$operator))])))
deprecated = sort(unique(c(unlist(stan_lang$deprecated), names(stan_lang$functions[sapply(stan_lang$functions, function(x) isTRUE(x$deprecated) & !isTRUE(x$operator))]))))
distributions = sort(unique(names(stan_lang$functions[sapply(stan_lang$functions, function(x) !isTRUE(x$deprecated) & !is.null(x$sampling))])))
reserved = c(unlist(stan_lang$reserved$stan), unlist(stan_lang$reserved$cpp))

funcs = names(stan_lang$functions[!sapply(stan_lang$functions, function(x) isTRUE(x$operator) | isTRUE(x$deprecated) | isTRUE(x$keyword))])

types = sort(unique(unlist(stan_lang$types)))
controls = unlist(stan_lang$keywords$control)
blocks = unlist(stan_lang$blocks)

## Write to file in XML format
# keywords
x = unique(c(controls, blocks))
cat("<key>BBLMKeywordList</key>\n\t<array>\n", paste0("\t\t<string>", x, "</string>", collapse = '\n'), "\n\t</array>\n", file = 'names.xml')
# predefined names
x = c(types, reserved, distributions)
cat("<key>BBLMPredefinedNameList</key>\n\t<array>\n", paste0("\t\t<string>", x, "</string>", collapse = "\n"), "\n\t</array>\n", file = 'names.xml', append = TRUE)
