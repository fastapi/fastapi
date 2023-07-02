<?xml version="1.0" encoding="utf-8"?>
<!-- vim: set sts=2 sw=2: -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:math="http://exslt.org/math" xmlns:str="http://exslt.org/strings">
  <xsl:output method="text"/>
  <xsl:template match="/mypy-report-index">
    <!-- It's possible to output without the <xsl:text> but it's harder to control. -->
    <xsl:text>Mypy Type Check Coverage Summary&#10;</xsl:text>
    <xsl:text>================================&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>Script: </xsl:text><xsl:value-of select="@name"/><xsl:text>&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>

    <xsl:variable name="max_module_width">
      <xsl:for-each select="file">
        <xsl:sort select="string-length(@module)" data-type="number"/>
        <xsl:if test="position() = last()">
          <xsl:value-of select="string-length(@module)"/>
        </xsl:if>
      </xsl:for-each>
    </xsl:variable>
    <xsl:variable name="max_imprecision_width" select="string-length('100.00% imprecise')"/>
    <xsl:variable name="max_loc_width" select="string-length(concat(sum(file/@total), ' LOC'))"/>

    <xsl:text>+-</xsl:text>
    <xsl:value-of select="str:padding($max_module_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_imprecision_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_loc_width, '-')"/>
    <xsl:text>-+&#10;</xsl:text>

    <xsl:text>| </xsl:text>
    <xsl:value-of select="'Module'"/>
    <xsl:value-of select="str:padding($max_module_width - string-length('Module'), ' ')"/>
    <xsl:text> | </xsl:text>
    <xsl:value-of select="'Imprecision'"/>
    <xsl:value-of select="str:padding($max_imprecision_width - string-length('Imprecision'), ' ')"/>
    <xsl:text> | </xsl:text>
    <xsl:value-of select="'Lines'"/>
    <xsl:value-of select="str:padding($max_loc_width - string-length('Lines'), ' ')"/>
    <xsl:text> |&#10;</xsl:text>

    <xsl:text>+-</xsl:text>
    <xsl:value-of select="str:padding($max_module_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_imprecision_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_loc_width, '-')"/>
    <xsl:text>-+&#10;</xsl:text>

    <xsl:for-each select="file">
      <xsl:variable name="score" select="(@imprecise + @any) div (@total + not(number(@total)))"/>
      <xsl:variable name="imprecision" select="concat(format-number($score, '0.00%'), ' imprecise')"/>
      <xsl:variable name="lines" select="concat(@total, ' LOC')"/>

      <xsl:text>| </xsl:text>
      <xsl:value-of select="@module"/>
      <xsl:value-of select="str:padding($max_module_width - string-length(@module), ' ')"/>
      <xsl:text> | </xsl:text>
      <xsl:value-of select="str:padding($max_imprecision_width - string-length($imprecision), ' ')"/>
      <xsl:value-of select="$imprecision"/>
      <xsl:text> | </xsl:text>
      <xsl:value-of select="str:padding($max_loc_width - string-length($lines), ' ')"/>
      <xsl:value-of select="$lines"/>
      <xsl:text> |&#10;</xsl:text>
    </xsl:for-each>

    <xsl:text>+-</xsl:text>
    <xsl:value-of select="str:padding($max_module_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_imprecision_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_loc_width, '-')"/>
    <xsl:text>-+&#10;</xsl:text>

    <xsl:variable name="total" select="sum(file/@total)"/>
    <xsl:variable name="score" select="(sum(file/@imprecise|file/@any)) div ($total + not(number($total)))"/>
    <xsl:variable name="imprecision" select="concat(format-number($score, '0.00%'), ' imprecise')"/>
    <xsl:variable name="lines" select="concat($total, ' LOC')"/>

    <xsl:text>| </xsl:text>
    <xsl:value-of select="'Total'"/>
    <xsl:value-of select="str:padding($max_module_width - string-length('Total'), ' ')"/>
    <xsl:text> | </xsl:text>
    <xsl:value-of select="str:padding($max_imprecision_width - string-length($imprecision), ' ')"/>
    <xsl:value-of select="$imprecision"/>
    <xsl:text> | </xsl:text>
    <xsl:value-of select="str:padding($max_loc_width - string-length($lines), ' ')"/>
    <xsl:value-of select="$lines"/>
    <xsl:text> |&#10;</xsl:text>

    <xsl:text>+-</xsl:text>
    <xsl:value-of select="str:padding($max_module_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_imprecision_width, '-')"/>
    <xsl:text>-+-</xsl:text>
    <xsl:value-of select="str:padding($max_loc_width, '-')"/>
    <xsl:text>-+&#10;</xsl:text>
  </xsl:template>
</xsl:stylesheet>
