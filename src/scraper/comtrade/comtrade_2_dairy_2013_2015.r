#install.packages("rjson")
library(rjson)

setwd("C:/Users/Suzanne/workspace/DATAS_Code/src/scraper/comtrade/")
#yearlist<-c("2010","2011","2012","2013","2014","2015")
yearlist<-c("201510","201511","201512")
HS_option<-"04"
animal_year<-"dairy_2015"

string <- "http://comtrade.un.org/data/cache/reporterAreas.json"
reporters <- fromJSON(file=string)
reporters <- as.data.frame(t(sapply(reporters$results,rbind)))

string <- "http://comtrade.un.org/data/cache/partnerAreas.json"
partners <- fromJSON(file=string)
partners <- as.data.frame(t(sapply(partners$results,rbind)))


string <- "http://comtrade.un.org/data/cache/classificationHS.json"
HSCodes <- fromJSON(file=string)
HSCodes <- as.data.frame(t(sapply(HSCodes$results,rbind)))

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

get.Comtrade <- function(url="http://comtrade.un.org/api/get?"
                         ,maxrec=50000
                         ,type="C"
                         ,freq="A"
                         ,px="HS"
                         ,ps="now"
                         ,r
                         ,p
                         ,rg="all"
                         ,cc="TOTAL"
                         ,fmt="csv"
)
{
  string<- paste(url
                 ,"max=",maxrec,"&" #maximum no. of records returned
                 ,"type=",type,"&"  #type of trade (c=commodities)
                 ,"freq=",freq,"&"  #frequency
                 ,"px=",px,"&"      #classification
                 ,"ps=",ps,"&"      #time period
                 ,"r=",r,"&"        #reporting area
                 ,"p=",p,"&"        #partner country
                 ,"rg=",rg,"&"      #trade flow
                 ,"cc=",cc,"&"      #classification code
                 ,"fmt=",fmt        #Format
                 ,sep = ""
  )
  print(string)
  
  if(fmt == "csv") {
    raw.data<- read.csv(string,header=TRUE)
    return(list(validation=NULL, data=raw.data))
  } else {
    if(fmt == "json" ) {
      raw.data<- fromJSON(file=string)
      data<- raw.data$dataset
      validation<- unlist(raw.data$validation, recursive=TRUE)
      ndata<- NULL
      if(length(data)> 0) {
        var.names<- names(data[[1]])
        data<- as.data.frame(t( sapply(data,rbind)))
        ndata<- NULL
        for(i in 1:ncol(data)){
          data[sapply(data[,i],is.null),i]<- NA
          ndata<- cbind(ndata, unlist(data[,i]))
        }
        ndata<- as.data.frame(ndata)
        colnames(ndata)<- var.names
      }
      return(list(validation=validation,data =ndata))
    }
  }
}
headers<-c('Classification','Year','Period','Period Desc.','Aggregate Level','Is Leaf Code',
           'Trade Flow Code','Trade Flow','Reporter Code','Reporter','Reporter ISO',	
           'Partner Code','Partner','Partner ISO','Commodity Code','Commodity','Qty Unit Code',
           'Qty Unit','Qty','Netweight (kg)','Trade Value (US$)','Flag')
logheaders<-c("reporter Text","report list","year","Code List","Empty Yes/No")


t<-t(headers)

tlog<-t(logheaders)

setwd("C:/Users/Suzanne/workspace/DATAS_Code/output_web/comtrade/")
today <- format(Sys.Date(), format="%Y_%m_%d")
newdir <- paste("", today, sep = "")
dir.create(newdir, showWarnings = FALSE)
setwd(newdir)


write.table(t,file=paste("comtrade_",animal_year,".csv",sep=""),row.names=FALSE, col.names=FALSE, sep=",")
write.table(tlog,file=paste("comtrade_log_",animal_year,".csv",sep=""),row.names=FALSE, col.names=FALSE, sep=",")

dfHSCodes<-data.frame(HSCodes)
colnames(dfHSCodes)<-c("HS6","HSText","HS4")

SelCodes<-dfHSCodes[substr(dfHSCodes$HS6,1,2)==HS_option,]
dfreporters<-data.frame(reporters)
colnames(dfreporters)<-c("Code","Text")

dfpartners<-data.frame(partners)
colnames(dfpartners)<-c("Code","Text")

exreplist<-c("40","56","58","100","191","196","203","200","208","233","697","492","246","890","251","276","292","300",
          "348","372","381","428","440","442","528","579","616","620","642","703","705","724","752","826","581","849","842","124")

dfreporters$exclude<-0

for (i in 1:nrow(dfreporters)){
    if(dfreporters$Code[i] %in% exreplist){dfreporters$exclude[i]<-1}
}
dfreporters<-dfreporters[dfreporters$exclude==0,]


parlist<-c("all","472","637","577","490","568","636","839")

dfpartners$exclude<-0

for (i in 1:nrow(dfreporters)){
  if(dfpartners$Code[i] %in% parlist){dfpartners$exclude[i]<-1}
}

dfpartners<-dfpartners[dfpartners$exclude==0,]


parlist<-""
for (i in 1:nrow(dfpartners)){
  parlist<-paste(parlist,dfpartners$Code[i],sep=",")
}    
for (z in (1:length(yearlist))){
  j<-2
  while ( j < nrow(dfreporters)) {
#  while ( j < 20) {  

    
    lj <-j+1
    print(lj)
  
    countrylist<-dfreporters$Code[lj]
    countryText<-dfreporters$Text[lj]
    if ((lj+4)< nrow(dfreporters)) {
      topj<-4
    } else {topj<-(nrow(dfreporters)-lj)}
  
    for (i in (lj+1):(lj+topj)){
      countrylist<-paste(countrylist,dfreporters$Code[i],sep=",")
      countryText<-paste(countryText,dfreporters$Text[i],sep=",")
    
    }
    j<-i
 
    k<-2

    lenselcode<-nrow(SelCodes)

    while (k < lenselcode) {
     ptime<-system.time({
      lk<-k+1
      codelist<-SelCodes$HS6[lk]
      if ((lk+13)< nrow(SelCodes)) {
        top<-13
      } else {top<-(nrow(SelCodes)-lk)}
  
      for (i in (lk+1):(lk+top)){
         codelist<-paste(codelist,SelCodes$HS6[i],sep=",")
       
      }

      k<-i

        s3 <- get.Comtrade(r=countrylist, p="all",rg="1,2,3,4", ps=yearlist[z],cc=codelist, freq="M")
        print(countrylist)
        print(codelist)
        tlog<-data.frame("CountryText" =character(1),"Countrylist" =character(1),"Year"=character(1),"Codelist"=character(1),"Datayn"=character(1))
        
        tlog$Datayn<-toString(is.null(colnames(s3$data)))

        tlog$CountryText<-  toString(countryText)
        tlog$Countrylist<-  toString(countrylist)
        tlog$Year<-toString(yearlist[z])
        tlog$Codelist<-toString(codelist)
        
        write.table(s3$data,file=paste("comtrade_",animal_year,".csv",sep=""),row.names = FALSE,col.names=FALSE,sep=",",append=TRUE)
        write.table(tlog,file=paste("comtrade_log_",animal_year,".csv",sep=""),row.names=FALSE, col.names=FALSE, sep=",",append=TRUE)
        
      })[3]
    
      if (ptime<36) {Sys.sleep(36-ptime) }

      print(ptime)
    
    } 
  }
}