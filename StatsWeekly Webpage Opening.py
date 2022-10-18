import webbrowser

webpage_list=['https://www.jstatsoft.org/index', 'https://journal.r-project.org/',
              'https://www.frontiersin.org/journals/applied-mathematics-and-statistics/articles',
              'https://journals.plos.org/plosone/browse/statistical_methods', 'https://www.nature.com/subjects/statistics',
              'https://www.sciencedaily.com/news/computers_math/statistics/', 'https://www.science.org/',
              'https://projecteuclid.org/journals/annals-of-statistics/current',
              'https://www.r-project.org/', 'https://blog.r-project.org/', 'https://www.python.org/blogs/','https://julialang.org/blog/',
              'https://blogs.sas.com/content/all-posts/', 'https://errorstatistics.com/', 'https://statmodeling.stat.columbia.edu/',
              'https://www.statisticshowto.com/', 'https://statisticsbyjim.com/blog/', 'https://www.theanalysisfactor.com/',
              'https://statanalytica.com/blog/', 'https://www.r-bloggers.com/']
              
new=True
for page in webpage_list:
    if new:
        webbrowser.open_new(page)
        new=False
    else:
        webbrowser.open_new_tab(page)



