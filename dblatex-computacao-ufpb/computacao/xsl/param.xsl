<?xml version='1.0' encoding="iso-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>

<!-- Add backmatter to the default layout -->
<xsl:param name="doc.layout">coverpage toc frontmatter mainmatter backmatter index </xsl:param>


<!-- DB2LaTeX has its own admonition graphics -->
<xsl:param name="figure.note">note</xsl:param>
<xsl:param name="figure.tip">tip</xsl:param>
<xsl:param name="figure.warning">warning</xsl:param>
<xsl:param name="figure.caution">caution</xsl:param>
<xsl:param name="figure.important">important</xsl:param>
<xsl:param name="admon.textlabel">0</xsl:param>
<xsl:param name="admon.graphics">1</xsl:param>


<!-- Adicionar número das páginas nas referencias, útil na versão impressa. -->
<xsl:param name="insert.xref.page.number">yes</xsl:param>

<!-- Options used for documentclass -->
<!-- Porque não usar twosides: http://tex.stackexchange.com/questions/42063/illogical-twoside-margins -->
<xsl:param name="latex.class.options">12pt,openright</xsl:param> 

<xsl:param name="latex.hyperparam">colorlinks=false,linkcolor=black,pdfstartview=FitH</xsl:param>
<!-- <xsl:param name="latex.hyperparam">linktocpage,colorlinks=false,linkcolor=black,pdfstartview=FitH</xsl:param> -->
<xsl:param name="paper.type">a4paper</xsl:param>
<xsl:param name="page.margin.bottom">1cm</xsl:param>
<xsl:param name="page.margin.top">1cm</xsl:param>
<xsl:param name="page.margin.inner">2.0cm</xsl:param>
<xsl:param name="page.margin.outer">2.0cm</xsl:param>
<xsl:param name="geometry.options"/>





<!-- DB2LaTeX requires Palatino like fonts -->
<xsl:param name="xetex.font">
  <xsl:text>\setmainfont{URW Palladio L}&#10;</xsl:text>
  <xsl:text>\setsansfont{FreeSans}&#10;</xsl:text>
  <xsl:text>\setmonofont{FreeMono}&#10;</xsl:text>
</xsl:param>

</xsl:stylesheet>
