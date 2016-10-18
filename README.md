# DATIX
Creating a modular data science workflow.
datix focuses on data.

## 1.0 DECLARATIVE CHARACTERIZATION OF DATA WORK

high level overview.

### 1.1 function application and composition

* pure ivory tower mumbo jumbo

### 1.2 sources, sinks, and transforms

* give the math-y stuff a more mechanized feel

### 1.3 extract, transform, load (ETL)

* relate abstract idea to enterprise-y stuff

### 1.4 summary

* these descriptions are very verb oriented.
* they are a very high level abstraction describing WHAT we are doing.
* notice that the section headings become more concrete.

## 2.0 ENTITIES OF DATA WORK

* how are the descriptions from section 1. implemented?
* what entities comprise them?

### 2.1 STORAGE/PERSISTANCE MECHANISM

* a 'persistance mechanism' can be read from, and written to.
* it is generally always possible to talk about its size as a function of time.
* examples:
   * filesystem
   * mysql
   * postgres
   * mssql
   * s3
   * dropbox
   * mongo
   * redis

###  2.2 DOCUMENT/DATAFRAME:

* immutable, static data.
* these are the objects read, and the objects written in section 2.1 above.
* they can be given a high level description - a type - a schema.
* closest representation of idea of a set.
* examples:
  * excel
  * pdf
  * worddoc
  * textfile
  * csv
  * json
  * image

### 2.3 COMPUTE ASSETS:

* physical or cloud infrastructure.
* example:
  * ec2
  * droplet
  * docker image

### 2.4 RUNTIMES/SERVICE PROVIDERS/PRODUCERS

* top level commodity.
* negative to zero impact on cashflow.
* it is possible to talk about its cost as a function of time.
* application running on compute instances.
* an object that performs a service on your behalf.
* contains untapped, unharvested data. requires code/flow to access
* examples:
  * aws
  * stripe
  * quickbooks
  * dropbox

### 2.5 CODE/FLOW:

* this is the work output by YOU

* examples:
  * node-RED flows
  * sql scripts
  * excel logic
  * etl scripts
  * scrapers

### 2.6 PRODUCT

* the thing YOU produce.
* zero to positive impact on cashflow

### 2.6 HOST

* the machine that datix CN runs on.
* this could be localhost.

## 3.0 USER INTERACTION

* adminLTE

## 4.0 PHILOSOPHY

* pos/neg port diagram.
* dashboard is open source.
* datix is a __way__ to view the world.
