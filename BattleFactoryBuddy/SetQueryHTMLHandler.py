# This class covers all the HTML construction for the "main" buddy functionality.
# This is created pretty much immediately after the query is received and is used to update the dictionary passed back to the django plumbing
# and on into the HTML doc rendered in the users browser.
# There's two main cases here:
# - Something goes wrong in the query and this builds an error message.
# - The query completes and this builds the output.
# As such it's got a big chunk of templates and the logic for how to populate them from a Results object passed from the SetQueryHandler.
#
class SetQueryHTMLHandler:
    # HTML for the top container that holds results. This makes sure things are a sensible size. Takes input
    # - Notes.
    # - Top Table
    # - Concertina container
    topContainer = "<div generatedHTML>{}{}{}<hr></div generatedHTML>"

    # HTML wrapping any text notes provided. Takes input:
    # - String
    topNotes = '<font size="1">{}.</font><br>'

    # HTML wrapping for any error text provided. Takes input:
    # - String
    errorNotes = '<font size="20"><b>{} </b></font><br>'

    # HTML stating that no matches are found. Takes no inputs.
    noMatches = '<font size="20"><b>No matches found, check inputs!</b></font><br>'

    # HTML for a tooltip. Takes inputs:
    # - The value that goes in the tooltip
    # - The text that is hover overable
    tooltip = """<a data-container="body" data-toggle="popover" html="true" width="500px" data-html="true" title="{}">{}</a>"""

    # HTML for the top Table on a successful result. Takes 2 inputs:
    # - Header for the column that is chance or phrase info.
    # - IV value for the Speed header
    # - An arbitrary number of rows to go in the table.
    detailTable = """<table class="table w-auto" style="margin-left:10px;">
  <thead>
    <tr>
      <th scope="col" style="left-margin:10px;">Name</th>
      <th scope="col">{}</th>
      <th scope="col">Item</th>
      <th scope="col"style="border-left: 1px solid LightGrey">Move 1</th>
      <th scope="col">Move 2</th>
      <th scope="col">Move 3</th>
      <th scope="col">Move 4</th>
      <th scope="col"style="border-left: 1px solid LightGrey">Nature</th>
      <th scope="col">EVs</th>
      <th scope="col">Speed ({}iv)</th>
    </tr>
  </thead>
  <tbody>
    {}    
  </tbody>
</table> 
"""

    # HTML for the table rows in the top table. Takes a tuple output by Set.GetTableRow.
    detailTableRow = """<tr>     
      <td><b><a data-container="body" data-toggle="popover" html="true" width="500px" data-html="true" title="{}">{}</a></b></td>
      <td><b><a data-container="body" data-toggle="popover" html="true" width="500px" data-html="true" title="{}">{}</a></b></td>      
      <td>{}</a></td>
      <td style="border-left: 1px solid LightGrey">{}</td>
      <td>{}</td>
      <td>{}</td>
      <td>{}</td>
      <td style="border-left: 1px solid LightGrey">{}</td>
      <td>{}</td>     
      <td>{} </td>
    </tr>"""

    # HTML for the 3 collapsible concertinas, including values in the headers and contents. Inputs here are a little complex:
    # - 3 different inputs cover whether each container is expanded or not. Handled by prePrepConcertinaArgsList
    # - The count to go with the header
    # - The body that goes in the container.
    tripleColumnsWithConcertina = """
        <div class="row">
            <div class="col" style="max-width:380px"> 
                <div class="accordion" id="accordionOne">
                    <div class="accordion-item" style="margin-left:10px;">
                        <h2 class="accordion-header" id="headingOne">
                            <button class="accordion-button {}" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="{}" aria-controls="collapseOne">
                                Very likely (>20%):&nbsp;<b>{} found</b>
                            </button>
                        </h2>
                        <div id="collapseOne" class="accordion-collapse collapse {}" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                            {} 
                            </div>
                        </div>                        
                    </div>
                </div>
            </div>
            <div class="col" style="max-width:380px"> 
                <div class="accordion" id="accordionTwo">
                    <div class="accordion-item" style="margin-left:10px;">
                        <h2 class="accordion-header" id="headingTwo">
                            <button class="accordion-button {}" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="{}" aria-controls="collapseTwo">
                                Likely (>4%):&nbsp;<b>{} found</b>
                            </button>
                        </h2>
                        <div id="collapseTwo" class="accordion-collapse collapse {}" aria-labelledby="headingThree" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                            {} 
                            </div>
                        </div>                        
                    </div>
                </div>
            </div>
            <div class="col" style="max-width:380px"> 
                <div class="accordion" id="accordionThree">
                    <div class="accordion-item" style="margin-left:10px;">
                        <h2 class="accordion-header" id="headingThree">
                            <button class="accordion-button {}" type="button" data-bs-toggle="collapse" data-bs-target="#collapseThree" aria-expanded="{}" aria-controls="collapseThree">
                                Possible (<4%):&nbsp;<b>{} found</b>
                            </button>
                        </h2>
                        <div id="collapseThree" class="accordion-collapse collapse {}" aria-labelledby="headingThree" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                            {} 
                            </div>
                        </div>                        
                    </div>
                </div>
            </div>                        
        </div>"""

    singleColumnWithConcertina = """
        <div class="row">
            <div class="col" style="max-width:1400px"> 
                <div class="accordion" id="accordionOne">
                    <div class="accordion-item" style="margin-left:10px;">
                        <h2 class="accordion-header" id="headingOne">
                            <button class="accordion-button {}" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="{}" aria-controls="collapseOne">
                                Possible sets left:&nbsp;<b>{} found</b>
                            </button>
                        </h2>
                        <div id="collapseOne" class="accordion-collapse collapse {}" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                            {} 
                            </div>
                        </div>                        
                    </div>
                </div>
            </div>"""
    # HTML for the table in the concertina that usually covers potential mons in the back. Takes inputs:
    # - HTML for the table rows.
    shortTable = """<table class="table table-sm" style="padding : 5%">
  <thead>
    <tr>
      <th scope="col">Species</th>
      <th scope="col">Chance</th>      
    </tr>
  </thead>
  <tbody>
    {}    
  </tbody>
</table>"""

    # HTML for each row of a table in the concertina sections.
    shortTableRow = """<tr>      
      <td>{}</td>
      <td>{}%</td>      
    </tr>"""

    # Blank initialise. Inputdict can change between creation and needing to actually build anything so we leave it blank.
    def __init__(self):
        pass

    # Build the HTML. Most useful comments about flow are covered in the HTML snippets above so aren't covered
    # again per-method.
    def buildHTML(self, inputdict, results):
        self.inputdict = inputdict
        self.results = results
        self.level = int(inputdict["Level"])
        self.ivs = int(inputdict["Battle"])
        if self.ivs == 15 and inputdict["Round"] in ("6", "8"):
            self.ivs = 31        
        self.inputdict["outputhtml"] = self.populateTopContainer()
        return self.inputdict

    # Method to put the finishing touches on the dynamic HTML by pieceing together any notes, the top table and
    # concertina sections.
    def populateTopContainer(self):
        # If we've an error or don't have any teams then just kick out an error.
        if self.results.errorNotes != []:
            return self.topContainer.format(self.populateErrorNotes(), "", "")
        elif not self.results.isValidTeams():
            return self.topContainer.format(self.noMatches, "", "")

        # We've got some legit results. Work out our 3 standard inputs.
        notes = self.populateNotes()
        toptable = self.populateTopTable()
        concertina = self.populateConcertina()

        return self.topContainer.format(notes, toptable, concertina)

    # Notes Section
    def populateNotes(self):
        if len(self.results.notes) > 0:
            return self.topNotes.format("<br>".join(self.results.notes))
        else:
            return ""

    # TODO make this properly handle a list of strings.
    def populateErrorNotes(self):
        return self.errorNotes.format(self.results.errorNotes[0])

    # Top Table
    def populateTopTable(self):
        if (
            (self.inputdict["Species1"] == "")
            and (self.inputdict["Species2"] == "")
            and (self.inputdict["Species3"] == "")
        ):
            return ""
        headerValue = "Chance"
        speedIV = self.ivs
        rows = self.populateTopTableRows()
        return self.detailTable.format(headerValue, speedIV, rows)

    def populateTopTableRows(self):
        rowList = []
        addDivider = False
        for speciesResult in self.results.iterGetConfirmedOpponentSpeciesResults():
            # We add a divider between mons but not before the first one.
            if not addDivider:
                addDivider = True
            else:
                rowList.append(
                    self.detailTableRow.format("","", "", "", "", "", "", "", "", "", "", "")
                )
            # Populate each table row
            for probability, set in speciesResult.iterGetSets():
                row = set.getTableRow(self.level, self.ivs, probability)
                rowList.append(self.detailTableRow.format(*row))
        return "".join(rowList)

    # Concertina
    # Work out what concertina layout we want. Generally this is:
    # - Nothing if we've been given all 3 mons up front.
    # - 3 columns if we're showing odds.
    # - 1 column if we're not/
    def populateConcertina(self):
        # If we've got 3 defined mons then we don't need the concertinas.
        if (
            (self.inputdict["Species1"] != "")
            and (self.inputdict["Species2"] != "")
            and (self.inputdict["Species3"] != "")
        ):
            return ""
        # If it's a Noland battle we don't need the concertinas.
        elif self.inputdict["Battle"] == "15" and "HiRes" not in self.inputdict:
            return ""
        elif "setleveldetail" in self.inputdict:
            return self.populateSingleConcertina()
        else:
            return self.populateTripleConcertina()

    def populateTripleConcertina(self):
        counts = [0, 0, 0]
        rows = [[], [], []]
        # Pull out our free agent results in order and add them to lists given by the buckets
        # we show in the GUI.
        for (
            speciesResult,
            speciesPercentage,
        ) in self.results.iterGetSortedFreeAgentSpeciesResults():
            if speciesPercentage > 20:
                idx = 0
            elif speciesPercentage > 4:
                idx = 1
            else:
                idx = 2
            counts[idx] += 1
            rowList = []
            for probability, set in speciesResult.iterGetSets():
                if "HiRes" not in self.inputdict or self.inputdict["Species1"] == "":
                    rowList.append(set.getTooltipInfo(probability * speciesPercentage / 100))
                else:
                    rowList.append(set.getTooltipInfo(probability))                        
            tooltip = "\n".join(rowList)
            rows[idx].append(
                self.shortTableRow.format(
                    self.tooltip.format(tooltip, speciesResult.speciesName),
                    "{:.2f}".format(speciesPercentage),
                )
            )

        # Work out which containers to show automatically. Current plan is that we show "Very likely"
        # if there's any entries and "Likely if there's fewer than 12".
        expandConcertina = [False, False, False]
        if counts[0] > 0:
            expandConcertina[0] = True
        if counts[1] > 0 and counts[1] < 12:
            expandConcertina[1] = True

        # Rationalize our text, "None found" reads better than "0 found".
        countStrs = []
        for count in counts:
            countStrs.append(str(count) if count != 0 else "None")

        # Create the concertina contents. That's a table if there's any entries of "Nothing to see here"
        tables = []
        for rowList in rows:
            if len(rowList) > 0:
                tables.append(self.shortTable.format("".join(rowList)))
            else:
                tables.append("Nothing to see here!")
        preppedConcertinas = self.prePrepTripleColumnWithConcertina(*expandConcertina)
        return preppedConcertinas.format(
            countStrs[0], tables[0], countStrs[1], tables[1], countStrs[2], tables[2]
        )

    def populateSingleConcertina(self):
        speedIV = self.ivs
        rowlist = []
        rowcount = 0
        # Create the table to go in the concertina.
        if "setleveldetail" in self.inputdict:
            sortablerowlist = []
            for (
                speciesResult,
                speciesPercentage,
            ) in self.results.iterGetSortedFreeAgentSpeciesResults():
                for probability, set in speciesResult.iterGetSets():                    
                    if "HiRes" not in self.inputdict or self.inputdict["Species1"] == "":
                        setprob = probability * speciesPercentage / 100
                    else:
                        setprob = probability                        
                    row = set.getTableRow(self.level, self.ivs, setprob)
                    sortablerowlist.append((setprob,self.detailTableRow.format(*row)))
                    
                    rowcount += 1
            sortablerowlist.sort(key=lambda tuple: tuple[0], reverse=True)
            for (probability, row) in sortablerowlist:
                rowlist.append(row)        
            table = self.detailTable.format("Odds", speedIV, "".join(rowlist))
        else: 
            for (
                speciesResult,
                unusedVar1,
            ) in self.results.iterGetSortedFreeAgentSpeciesResults():
                for unusedvar2, set in speciesResult.iterGetSets():
                    row = set.getTableRow(self.level, self.ivs, "")
                    rowlist.append(self.detailTableRow.format(*row))
                    rowcount += 1
            table = self.detailTable.format("Phrase", speedIV, "".join(rowlist))

        # Create the concertina, populating with the table and the count. We can assume there
        # are results here, as otherwise we would have just returned nothing from populateConcertina
        # rather than calling into here.
        show = rowcount < 12
        preppedConcertina = self.prePrepSingleColumnWithConcertina(show)
        concertina = preppedConcertina.format(str(rowcount), table)
        return concertina

    # It's a bit awkward to handle the triple concertina as it needs multiple HTML tags in sync. This utility method
    # handles that (and the HTML syntax) so the calling function can just provide the data.
    def prePrepTripleColumnWithConcertina(self, showFirst, showSecond, ShowThird):
        argslist = []
        for show in (showFirst, showSecond, ShowThird):
            # Cover the Button Html
            argslist += self.prePrepConcertinaArgsList(show)
        return self.tripleColumnsWithConcertina.format(*argslist)

    def prePrepSingleColumnWithConcertina(self, show):
        argslist = self.prePrepConcertinaArgsList(show)
        return self.singleColumnWithConcertina.format(*argslist)

    def prePrepConcertinaArgsList(self, show):
        argslist = []
        if show:
            argslist.append("")
            argslist.append("true")
        else:
            argslist.append("collapsed")
            argslist.append("false")
        # Add the format indicator back in.
        argslist.append("{}")
        # Cover the Table Html
        if show:
            argslist.append("show")
        else:
            argslist.append("hide")
        # Add the format indicator back in.
        argslist.append("{}")
        return argslist
