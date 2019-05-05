# Ebook_Collection
> This project was a part of [Gargantua Project](https://gitlab.com/gargantua), Promote **Global Free Study** 

This project was made to catch the ebook resources

## Structure

```txt
|
|--crawler1
|    |
|    |--crawler program
|    |
|    |--database
|    |
|--crawler2
|    |
|    |--crawler program
|    |
|    |--database
|    |
|--crawler...
|...
|
|--basic function 
|
```

## DataBase
> the database will be public in 2020 

**Table**: book

**Value:**
1. **Book name**
2. **Resource address**
3. **Download link**
4. **Introduction**

## Develop Guide

### Step 1: Create a project file

Once you want to create a project, just create a fold in the `ebook_collection`, and named the fold as your wish. and in the later programming, you Have to add all your stuff inside the fold you create.

### Step 2: Coding:

Yes, you can coding now! 

To convenience your coding  experience, we also make some basic function, and they are all in the `basic.py`, below listed the function you can called:

**Provided function:**

Once you want to use the basic function we provided, import basic in your code:

```python
import basic
```

The `basic` function provided you two main tool: `crawler` and `database manipulate`, and we will first talk about the crawler component

**Crawler Component:**

 ```python
import basic

# create a crawler tool
crawler_tool = basic.crawlerComponent()

# get an random IP
ip = crawler_tool.get_an_ip()

# get a header
headers = crawler.get_crawel_header()
 ```

**Database:**

1. build a new database:

```python
import basic

# create a tool
tool = basic.tools()

# remove the current database
tool.remove_database()

# create a database tool
database_tool = basic.dataBase()

# build a new database
database.build_database()
```

2. add a `book` into the database:

```py
import basic

database_tool = basic.dataBase()

book = [
         ['name1','link1','direct_link1','introduction1'],             		          ['name2','link2','direct_link2','introduction2']
       ]
       
database_tool.add_book(book)
```

3. display the first 5 book:

```py
import basic

database_tool = basic.dataBase()

database_tool.head()
```



## Contribute
1. fork
2. add your book crawler
3. pull request **WITHOUT** push the database
4. [email](mailto://p@hty.email) your **INDIVIDUAL** database
5. after check the quality of your individual database, If its ok, I will merge the it in to the main database

transfer your book's dataBase