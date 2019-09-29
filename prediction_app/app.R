# Imports
library(shiny)
library(tidyverse)
library(ggplot2)
library(ggthemes)
library(DT)
library(shinythemes)
library(shinydashboard)

# Set Working Directory
setwd('/Users/chrisfeller/Desktop/League_Strength/prediction_app/')

# Read in predictions
prediction_df <- read.csv('data/predictions.csv', check.names=FALSE)
ranking_df <- prediction_df %>%
                group_by(LEAGUE) %>%
                summarise(MEDIAN_PREDICTION=round(median(PREDICTION), 3)) %>%
                arrange(desc(MEDIAN_PREDICTION))


ui <- dashboardPage(skin = 'blue', 
    dashboardHeader(title = 'League Strength', titleWidth = 1700),
    
    dashboardSidebar(
      selectInput("league1", h3("League 1"),
                  choices = sort(unique(prediction_df$LEAGUE)),
                  selected = 'NBA'),
      selectInput('league2', h3('League 2'),
                  choices = sort(unique(prediction_df$LEAGUE)),
                  selected = 'Chinese CBA')
    ), 
    
    dashboardBody(  
      fluidRow(
      column(4,
             DT::dataTableOutput('table')), 
      
      column(8,
             br(),
             br(),
             plotOutput("plot"))
      )
    )
  )
    
server <- function(input, output){
  output$table <- DT::renderDataTable(
    ranking_df, 
    options = list(lengthChange = FALSE,
                   pageLength = 20, 
                   searching = FALSE))  
  
  output$plot <- renderPlot({
      ggplot(prediction_df %>% filter(LEAGUE %in% c(input$league1, input$league2)), aes(x=PREDICTION, fill=LEAGUE)) +
      geom_density(alpha=.3)})

}



  
shinyApp(ui = ui, server = server)