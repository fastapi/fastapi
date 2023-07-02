<?xml version="1.0" encoding="utf-8"?>
<!-- vim: set sts=2 sw=2: -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:param name="ext" select="'xml'"/>
  <xsl:output method="html"/>
  <xsl:variable name="xml_stylesheet_pi" select="string(//processing-instruction('xml-stylesheet'))"/>
  <xsl:variable name="stylesheet_name" select="substring($xml_stylesheet_pi, 23, string-length($xml_stylesheet_pi) - 28)"/>
  <xsl:template match="/mypy-report-index">
    <html>
      <head>
        <link rel="stylesheet" type="text/css" href="{$stylesheet_name}.css"/>
      </head>
      <body>
        <h1>Mypy Type Check Coverage Summary</h1>
        <table class="summary">
          <caption>Summary from <xsl:value-of select="@name"/></caption>
          <thead>
            <tr class="summary">
              <th class="summary">File</th>
              <th class="summary">Imprecision</th>
              <th class="summary">Lines</th>
            </tr>
          </thead>
          <tfoot>
            <xsl:variable name="bad_lines" select="sum(file/@imprecise|file/@any)"/>
            <xsl:variable name="total_lines" select="sum(file/@total)"/>
            <xsl:variable name="global_score" select="$bad_lines div ($total_lines + not(number($total_lines)))"/>
            <xsl:variable name="global_quality" select="string(number(number($global_score) &gt; 0.00) + number(number($global_score) &gt;= 0.20))"/>
            <tr class="summary summary-quality-{$global_quality}">
              <th class="summary summary-filename">Total</th>
              <th class="summary summary-precision"><xsl:value-of select="format-number($global_score, '0.00%')"/> imprecise</th>
              <th class="summary summary-lines"><xsl:value-of select="$total_lines"/> LOC</th>
            </tr>
          </tfoot>
          <tbody>
            <xsl:for-each select="file">
              <xsl:variable name="local_score" select="(@imprecise + @any) div (@total + not(number(@total)))"/>
              <xsl:variable name="local_quality" select="string(number(number($local_score) &gt; 0.00) + number(number($local_score) &gt;= 0.20))"/>
              <tr class="summary summary-quality-{$local_quality}">
                <td class="summary summary-filename"><a href="{$ext}/{@name}.{$ext}"><xsl:value-of select="@module"/></a></td>
                <td class="summary summary-precision"><xsl:value-of select="format-number($local_score, '0.00%')"/> imprecise</td>
                <td class="summary summary-lines"><xsl:value-of select="@total"/> LOC</td>
              </tr>
            </xsl:for-each>
          </tbody>
        </table>
      </body>
    </html>
  </xsl:template>
  <xsl:template match="/mypy-report-file">
    <html>
      <head>
        <link rel="stylesheet" type="text/css" href="{$stylesheet_name}.css"/>
      </head>
      <body>
        <h2><xsl:value-of select="@module"/></h2>
        <table>
          <caption><xsl:value-of select="@name"/></caption>
          <tbody>
            <tr>
              <td class="table-lines">
                <pre>
                  <xsl:for-each select="line">
                    <span id="L{@number}" class="lineno"><a class="lineno" href="#L{@number}"><xsl:value-of select="@number"/></a></span><xsl:text>&#10;</xsl:text>
                  </xsl:for-each>
                </pre>
              </td>
              <td class="table-code">
                <pre>
                  <xsl:for-each select="line">
                    <span class="line-{@precision}" title="{@any_info}"><xsl:value-of select="@content"/></span><xsl:text>&#10;</xsl:text>
                  </xsl:for-each>
                </pre>
              </td>
            </tr>
          </tbody>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
