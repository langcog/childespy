# A Python API for childes-db

The `childespy` package allows you to access data in the childes-db from Python. This removes the need to write complex SQL queries in order to get the information you want from the database.

This package is a wrapper for the latest version of the `childesr` R package (https://github.com/langcog/childesr), so it requires the user to install R (>=3.6) on their machine. Instructions can be found here: https://www.r-project.org/.

`childesr` has R [package dependencies, listed here](https://github.com/langcog/childesr/blob/master/DESCRIPTION), which `childespy` will automatically install.
