# Chapter 1 - Data Warehousing, Business Intelligence, and Dimensional Modeling Primer

### Overall Comments
This chapter can be read at several different levels. It is possible to read this
chapter as a DBA/DA/AE purely for direction on the best way to model data. It can
also be read as a data manager or strategist who thinks about the philosophical
underpinnings of data teams. By the third page I found myself messaging
my Director to get her thoughts on areas where our organization is using operational
tools to serve BI needs, the reverse, and which one is worse. Anyone who works in
data will get immense value from reading (and rereading) this chapter.

### One Sentence Summary
Dimensional modeling is an effective technique to create simple data structures
that are easily understood by business users, and, in conjunction with an appropriate
architectural philosophy, have historically enabled organizations to leverage the
data they capture to make better decisions.

## Questions Discussed in This Chapter 

- What business outcomes are achieved by data warehousing and business intelligence?
- What is dimensional modeling?
- What is the Kimball architecture and what are some alternatives?
- What are some common misconceptions about dimensional modeling?

### What business outcomes are achieved by data warehousing and business intelligence?
The phrasing of the question makes an important assumption that the authors
explicitly state in the first paragraph of the chapter: 
>You may be disappointed to learn that we don't start with technology and 
tools - first and foremost, the DW/BI system must consider the needs of the 
business. With the business needs firmly in hand, we work backwards through the 
logical and then physical designs, along with decisions about technology and tools.

This is a good assumption to make, but an important one to note: _DW/BI exists
solely to serve the needs of the business._ The authors list the requirements
that must be met in order for the DW/BI system to fully meet the needs of the business.
The DW/BI system must...
- make information easily accessible
- present information consistently
- adapt to change
- present information in a timely way
- a secure bastion that protects the information assets
- serve as the authoritative and trustworthy foundation for improved decision making
- be accepted by the business community

Okay, let's say we have a DW/BI system that hits all of those requirements. What
does the business get out of it? Since the benefits of each requirement are pretty 
self evident, the authors don't explicitly state what happens when they're all met.
To my mind, the better a DW/BI solution performs in each of the above dimensions,
the greater the ability of the organization to use the right information to make
decisions. I'm sure that upon further thought and reading I will find a better 
answer to the motivating question!

### What is dimensional modeling?
Dimensional modeling, also known as the star schema, is a technique used to enable fast query performance and
achieve database simplicity. It achieves this by partitioning individual occurences 
of business processes (facts) and important units of analysis (dimensions) into 
separate tables that are later joined together in a "star" structure. Multidimensional
environments, which allow business users to aggregate facts across multiple dimensions,
are referred to as OLAP (online analytical processing) cubes. Dimensional modeling
is distinguished from third normal form (3NF) modeling by denormalizing the schema.
This means that fewer tables, and thus fewer joins, will be required to answer
business questions.

At the time of the book's publication, dimensional modeling was the preferred
technique for presenting analytic data to customers. Because of advancements
in data warehousing technology, fast query performance can now be achieved without 
strict adherence to dimensional modeling ([here's](https://www.holistics.io/blog/the-rise-and-fall-of-the-olap-cube/) 
a recent article discussing the rise and fall of the OLAP cube). However, in my
opinion, the logical clarity and simplicity offered by the dimensional approach 
still provides a lot of value.

### What is the Kimball architecture and what are some alternatives?
The Kimball architecture is an implementation of a DW/BI structure that consists
of four components: source systems, an ETL system, a presentation area, and a BI
application. This architecture is designed to hide complicated parts of the 
DW/BI system from the end business user and present a clean, holistic view of the company's
information to business users.

Some traditional alternatives to the Kimball architecture are the data warehouse
approach and the Corporate Information Factory (CIF) approach. Both of these
approaches incorporate "data marts", which are designed for specific entities
within an organization, and are not meant for use outside of those departments.

[_Cloud Data Management_](https://dataschool.com/data-governance/), a more recent
and continuously-updated web book, recommends a different approach that has been
made possible by powerful cloud databases. I think this approach is definitely
the best practice now in 2020, but it's important to understand previous architectures
and the problems they were designed to solve.

### What are some common misconceptions about dimensional modeling?
The authors list five misconceptions about dimensional modeling:

- they're only for summary data
- they're departmental not enterprise
- they're not scalable
- they're only for predictable storage
- can't be integrated
