# Imports
library(shiny)
library(tidyverse)
library(ggplot2)
library(ggthemes)
library(DT)
library(shinythemes)
library(shinydashboard)

# Set Working Directory
# setwd('/Users/chrisfeller/Desktop/League_Strength/prediction_app/')

# Read in predictions
prediction_df <- read.csv('data/predictions.csv', check.names=FALSE) %>%
                          mutate(LEAGUE = str_replace(LEAGUE, '_', ' '))
# Calculate League Rankings
ranking_df <- prediction_df %>%
                group_by(LEAGUE) %>%
                summarise(MEDIAN_PREDICTION=round(median(PREDICTION), 3)) %>%
                arrange(desc(MEDIAN_PREDICTION)) %>%
                rename('MEDIAN PREDICTION' = MEDIAN_PREDICTION)


# Create dashboard user interface
ui <- dashboardPage(skin = 'blue', 
    dashboardHeader(title = 'League Strength', titleWidth = 1700),
    
    dashboardSidebar(
      br(),
      br(),
      p("To compare the strength of various leagues, select two seperate options 
        in the drop-down menus below:"),
      selectInput("league1", h3("League 1"),
                  choices = sort(unique(prediction_df$LEAGUE)),
                  selected = 'NBA'),
      selectInput('league2', h3('League 2'),
                  choices = sort(unique(prediction_df$LEAGUE)),
                  selected = 'Chinese CBA'),
      br(),
      p("Upon making your selection, the page will populate with a table and plot."), 
      br(),
      p("The table displays the strength of each league determined by the median predicted 
        NBA performance, in terms of Win Shares (WS), of all players within a respective league."),
      br(),
      p("The plot displays the distribution of predicted NBA performance for each 
        player in the two leagues selected above (blue and red distributions). The median prediction for 
        all players globally is represented by the dashed line."),
      br(),
      p('The default example, illustrates the strength of the NBA (blue) being greater than 
        both the Chinese CBA (red) in addition to the median player globally (dashed line).'),
      br(),
      HTML('<footer>
           <div align="center">
           <p>Chris Feller | chrisjfeller.com<p/>
           </div>
           </footer>')      
    ), 
    
    dashboardBody(  
      fluidRow(
      column(4,
             DT::dataTableOutput('table')), 
      
      column(8,
             br(),
             br(),
             br(),
             br(),
             br(),
             plotOutput("plot"))
      )
    )
  )
    
# Create dashboard server
server <- function(input, output){
  output$table <- DT::renderDataTable(
    ranking_df, 
    options = list(lengthChange = FALSE,
                   pageLength = 20, 
                   searching = FALSE))  
  
  output$plot <- renderPlot({
      ggplot(prediction_df %>% filter(LEAGUE %in% c(input$league1, input$league2)), aes(x=PREDICTION, fill=LEAGUE)) +
      xlim(-12, 12) +
      geom_density(alpha=.3) + 
      geom_vline(data=prediction_df, aes(xintercept=median(PREDICTION)),
                 linetype="dashed", size=.5, colour="black") + 
      labs(y = "Density", x = 'Win Share (WS) Prediction', fill='League') +
      annotate("text", label="Global Median", 
               x=.98, y=.001, vjust=0, hjust=0, angle = 90, size=5, face='bold') +
      ggtitle(sprintf('%s vs %s', input$league1, input$league2)) + 
      scale_fill_manual( values = c("red","dodgerblue")) + 
      theme_grey(15) + 
      theme(plot.title = element_text(size=20, hjust = 0.5, face = 'bold'))
      }, height = 600, width = 1050)
}
  
# Run app
shinyApp(ui = ui, server = server)