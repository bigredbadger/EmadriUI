library(shiny)
library(shinyjs)
library(shinythemes)
#library(shinydashboard)

library(DT)
# library(wordcloud2)

# devtools::install_github("yha2017/emadri3", force = TRUE)
library(emadri3)
library(anonymizer)
library(sentimentr)
library(exploratory)

library(reticulate)

library(stringdist)

# FUNCTION FOR GETTING WORD CLOUD
# getFreq <- function(pid) {
#   adjs <- data[data$product_id %in% pid, 5]
#   corpus <- Corpus(VectorSource(adjs))
#   dtm <- TermDocumentMatrix(corpus, control = list(minWordLength = 1))
#   m <- as.matrix(dtm)
#   m <- sort(rowSums(m), decreasing = TRUE)
#   freq <- data.frame(word = names(m), freq = m)
#   freq$word <- as.character(freq$word)
#   return(freq)
# }

data <- read.csv("sentiment_100000")
emadri <- read.csv("mini.csv")
source_python("OG.py")

emadriID <- function(pid) {
  id = 0
  min = 1
  id2 = 0
  min2 = 1
  adj <- data[data$product_id %in% pid, 'value']
  cat <- data[data$product_id %in% pid, 'item_name']
  adjs <- as.vector(rbind(as.character(adj), as.character(cat)))
  for (i in 1:nrow(emadri)) {
    tag = emadri[i, 'tag']
    all = T
    d = stringdist(tag, paste(adjs, collapse = " "), method = "jaccard")
    for (j in adjs) {
      if (!grepl(j, tag)) {
        if (d < min) {
          min = d
          id = emadri[i, 1]
        }
        all = F
        break
      }
    }
    if (all && d < min2) {
      min2 = d
      id2 = emadri[i, 1]
    }
  }
  if (id2 != 0) return(id2)
  else return(id)
}

shinyApp(
  ui = navbarPage("", id = "tabs", theme = shinytheme("yeti"),
    tabPanel("EMADRI", value = "tab1", class = "Landing",
      tags$style(HTML(".Landing{ 
                       background-image:url('https://www.emadri.com/images/inspire_bg.jpg');
                       width:100vw; height:calc(100vh - 45px); background-size:cover;
                       position:absolute; left:0; top:45px;}")),
      tags$head(includeScript("return.js")),
      tags$div(id = "Input",
        tags$style(HTML("#Input{text-align:center; position:absolute;
                        left:50%; top:25%; transform:translate(-50%,-50%);}")),
        tags$h1(id = "Title", "What's Up!"),
        tags$style(HTML("#Title{-webkit-user-select:none; -khtml-user-select:none;
                        -webkit-touch-callout:none; -moz-user-select:none;
                        -o-user-select:none; user-select:none; font-size:45px;}")),
        tags$p(textInput("text", "", width = 500,
                        placeholder = "What's in you mind? e.g., I need a blue dress!")),
        tags$p(actionButton("button", "Go!"))
      )
    ),
    tabPanel("Result", value = "tab2", useShinyjs(), extendShinyjs(script = "hide.js"),
      tags$style(HTML(".navbar-nav > li:nth-child(2) {position:absolute; right:5vw;}")),
      sidebarLayout(
        sidebarPanel(width = 3,
          tags$h2(id = "Title2", "What's Up!"),
          tags$style(HTML("#Title2{-webkit-user-select:none; -khtml-user-select:none;
                           -webkit-touch-callout:none; -moz-user-select:none;
                           -o-user-select:none; user-select:none;}")),
          textInput("text2", "", width = 375,
                    placeholder = "Changed your mind? Try again!"),
          actionButton("button2", "Go!")# ,
          # wordcloud2Output("plot", width = "30vw", height = "50vh"),
          # tags$style(HTML("#plot{position:absolute; top: 30vh;}"))
        ),
        mainPanel(width = 9,
          textOutput("textOutput"),
          dataTableOutput("tableOutput")
        )
      )
    )
  ),
  server = function(input, output, session) {
    idlist <- reactiveValues()
    observeEvent(input$button, {
      if (input$text != "") {
        shinyjs::show(selector = '#tabs li a[data-value="tab2"]', time = 0)
        updateNavbarPage(session, "tabs", "tab2")
        updateTextInput(session, "text", value = "")
        updateTextInput(session, "text2", value = input$text)
      }
    })
    observe({
      if (input$tabs == "tab1") {
        shinyjs::hide(selector = '#tabs li a[data-value="tab2"]', time = 0)
      }
    })
    output$textOutput <- renderText({
      input$button
      input$button2
      txt <- isolate(input$text2)
      chars <- unlist(strsplit(txt, ""))
      ltr <- sum((chars <= 'z' & chars >= 'a') | (chars <= 'Z' & chars >= 'A'))
      if (ltr > 2) idlist$id <- as.character(get_product_id(txt, data)$result)
      else idlist$id <- character(0)
      if (length(idlist$id) == 0) "No Result!"
    })
    output$tableOutput <- renderDataTable({
      input$button
      input$button2
      if (length(idlist$id) != 0) {
        outfit <- OutfitGeneratorDist(emadriID(idlist$id))
        outfit <- outfit[match(c("Outerwear", "Top", "Bottom", "Footwear", "Accessory"),
                               outfit$new_cat),]
        datatable(escape = F, rownames = F,
                  options = list(dom = 't',
                                 columnDefs = list(list(className = 'dt-center', targets = 0:5))),
                  data = data.frame(Brand = outfit$brand,
                                    Product = outfit$name,
                                    Category = outfit$new_cat,
                                    Price = paste0("$", format(outfit$price, trim = T, nsmall = 2)),
                                    Retailer = paste0("<a href='", outfit$retailer_url, "'>",
                                                      outfit$retailer_name, "</a>"),
                                    Image = paste0("<img src=image/", outfit$product_id, ".jpg",
                                                   " alt='Image Unavailable' height='150'></img>"))
        ) %>% formatStyle(columns = 0:5, fontSize = "110%", target = "row", backgroundColor = "white")
      }
    })
    # WORD CLOUD OF ADJECTIVES: NOT IN USE ANYMORE
    # output$plot <- renderWordcloud2({
    #   if (length(idlist$id) != 0) {
    #     freq <- getFreq(idlist$id)
    #     wordcloud2(freq,minRotation = -pi/3, maxRotation = pi/3, rotateRatio = 1,
    #                ellipticity = 1, gridSize = 1)
    #   }
    # })
  }
)