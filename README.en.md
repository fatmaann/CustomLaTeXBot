# CustomLaTeXBot [![ru](https://img.shields.io/badge/lang-ru-green.svg)](https://github.com/fatmaann/CustomLaTeXBot/blob/main/README.md)<br>
<b>Coursework - Documentation Generator "Mentors Joy".<br>
Telegram - bot for creating PDF GOST documentation for submitting diploma and coursework</b>.<br>
<b>Aiogram, Latex, PyLatex, Pdflatex.exe, Ngrok, Redis</b>

## Relevance

Documents often contain missing pages, template errors, incorrect indents - a complete lack of understanding of the basic elements necessary for proper documentation in a course / diploma project.<br><br>In response to this widespread problem, a `Telegram - bot` was developed, which provides users with the ability to use a constructor to generate `LaTeX` documents based on specified `JSON` templates. After filling out the form, based on the entered information and the template, the program generates the final
`PDF` and sends it to the user.

## Architecture of Telegram - bot

### Main library - <a href="https://aiogram.dev"><em><b>Aiogram</b></em></a>

In this project, <em>Callback Handling</em> plays an important role in the interaction between the user and the `Telegram` bot.
A callback is an interaction that occurs when the user presses a button from the built-in keyboard.
All interaction with the user before filling out the template occurs using the built-in keyboard.
<br>With its help, the format of the future document is selected, and chapters and subchapters are configured.

<table align="center">
<tr>
  <th colspan="3" align="left"">Select one of the formats:<br><br>1) Operator's manual<br>2) Programmer's manual<br>3) Technical specifications<br>4) Explanatory note<br>5) Test program and methodology<br>6) Program text<br><br></th>
</tr>
  <tr>
    <td align="center">1</td>
    <td align="center">2</td>
    <td align="center">3</td>
  </tr>
  <tr>
    <td align="center">4</td>
    <td align="center">5</td>
    <td align="center">6</td>
  </tr>
  <tr>
    <th colspan="3" align="center">Back</th>
  </tr>
</table>
<div align="center"><i>Defining a document outline</i></div><br>

<table align="center">
  <tr>
    <th colspan="2" align="left"">Document structure:<br>❌ Title page<br>❌ Abstract<br>✅ Purpose of the program<br>✅ Condition for program execution<br>✅ Program execution<br>✅ Messages to the operator<br>❌ List of terms and abbreviations<br><br>If there is a ✅ at the beginning of the line, you can customize (add or remove) subchapters in this chapter.<br>Chapters with a ❌ sign are not flexible in terms of the number of subchapters.<br><br>Select the chapters you want to change in the document by clicking the corresponding buttons below.<br>Otherwise, you can immediately create a document in the selected format.</th>
</tr>
  <tr>
    <td align="center">Change</td>
    <td align="center">Create</td>
  </tr>
  <tr>
    <th colspan="2" align="center">Back</th>
  </tr>
</table>
<div align="center"><i>Menu for selecting the future document format</i></div><br>

The bot also accepts messages to fill the selected template - messages containing `JSON` files used to compile them into `PDF` format.</b>

### Service commands

* `/start` - a command that defines the beginning of interaction with the bot.
* `/main_menu` - a command that allows you to quickly move to the main
menu of the bot interface.
* `/choose_format` - a command that allows you to quickly move to the menu
for choosing the future document format.
* `/send_file` - a command that allows you to quickly move to the main menu
for sending `JSON` format.
* `/help` - a command that allows you to receive a message with brief explanatory
information about the bot.

### Hosting 

<b><a href="https://ngrok.com/docs"><em>Ngrok</em></a></b> — a powerful tool that simplifies secure tunneling
to access local servers on the Internet.<br>Allows temporary public `URLs` to access your locally hosted applications or services.<br>
This feature is especially useful when developing web applications or working with webhooks in environments such as <b><em>Aiogram</em></b>.

<b><em>Ngrok</em></b> provides a secure public `URL` that forwards incoming requests from `Telegram` to a local <b><em>Aiogram</em></b> bot.


## Managing user data

The service provides the user with a flexible choice for setting up the future document.<br>It is necessary to think over a <ins><i>fast and reliable</i></ins> system for storing user data,<br>to track all the changes made by the user on the way to creating the file.<br>The data <ins><i>should be temporary</i></ins>, since there is no need to store data about the user if he does not return.<br>
<b><br>The <a href="https://redis.io"><em>Redis</em></a></b> database system is perfect for this purpose.<br>

<b><em>Redis</em></b> provides a unique feature known as `"expire"`. With this feature, developers can set a time to live (`TTL`) for each key-value pair in <b><em>Redis</em></b>. When the `TTL` expires, <b><em>Redis</em></b> <i><ins>automatically deletes the data</i></ins> from the database.<br><br>
<i><ins>The user profile is deleted or cleared</i></ins> as soon as the user receives a completed `PDF`, when exiting to the main menu, or if the program has not interacted with the user for
<i><ins>12 hours</i></ins>.<br><br>

## Compilation of PDF documents

<b><a href="https://jeltef.github.io/PyLaTeX/latest/pylatex/pylatex.document.html"><em>PyLatex</em></a></b> - python library that provides a convenient and intuitive way to programmatically generate `LaTeX` files.

### Features and benefits of the <b><em>Pylatex</b></em>
* Documents acquire a <b><i>complex structure</i></b>, including sections, divisions, paragraphs, and more.
* <b><i>Formatting and Style</i></b> - access to various formatting options<br>(font styles, colors, page layouts, and custom headers and footers, etc.).
* <b><i>Math Typesetting</i></b> - use expressions, symbols, matrices, and other mathematical constructs.
* <b><i>Bibliography and Citations</i></b> - integration with BibTeX, which allows you to easily manage bibliographies and citations in `LaTeX` documents.
* <b><i>Insert</i></b> images, tables, and visual elements into `LaTeX` documents.<br>

After populating the document class object with <b><em>PyLatex</em></b>, we talk to <ins><b>pdflatex.exe</b></ins> to compile the `LaTeX` document to `PDF`.

<b><em>PDF LaTeX</em></b> is an extension of the `LaTeX` typesetting system, specifically oriented towards creating output in `PDF` format.<br><br>
The <ins><b>pdflatex.exe</b></ins> file is part of the distributions: <b>MiKTeX, TeX Live, MacTeX</b>.<br>
