<?php

# $mysqli = new mysqli("localhost", "baselessdata_lyn", "thisIsPwd", "baselessdata_db");
$mysqli = new mysqli("localhost", "root", "root", "baselessdata_db");

if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}


$q = $_GET["q"];
$attr = $_GET["attr"];



if ($attr == "Gene No") {
    $sql = "SELECT * FROM `Gene` WHERE Gene_No = '$q' ORDER BY Gene_No";
}
else if ($attr == "Gene ID") {
    $sql = "SELECT * FROM `Gene` WHERE Gene_ID = '$q' ORDER BY Gene_ID";
}
else if ($attr == "Gene Symbol") {
    $sql = "SELECT * FROM `Gene` WHERE Gene_Symbol LIKE '%$q%' ORDER BY Gene_Symbol";
}
else if ($attr == "Gene Name") {
    $sql = "SELECT * FROM `Gene` WHERE Gene_Full_Name LIKE '%$q%' ORDER BY Gene_Full_Name";
}
else {
    $sql = "";
}


$result = $mysqli->query($sql);


print("<table width=\"100%\" border=\"1\" cellpadding=\"10\">
    <tr>
        <td  align=\"center\">
        <h1>Gene Information Database</h1>
        <h2> CS411 </h2>
        <h3>For Demo Purpose Only!</h3>
        <h4>Gene Search Result(s)</h4>
        </td>
    </tr> ");

print("<td>&nbsp;<a href=\"index.html\">Home</a> &nbsp;
     </td> ");

print("<tr>
        <td align=\"center\"> ");

        $num_rows = $result->num_rows;
        if ($num_rows > 0)
        {
            print("<p>There are " . $num_rows . " result(s) available</p>");
            while ($row = $result->fetch_assoc())
            {
                print("<p><b> Gene: {$row['Gene_No']} </b>");

                print("<br><br>");

                print("<b><u>Gene ID:</u></b> {$row['Gene_ID']}<br/>");
                print("<b><u>Gene Symbol:</u></b> {$row['Gene_Symbol']}<br/>");
                print("<b><u>Gene Name:</u></b> {$row['Gene_Full_Name']}<br/>");
                print("<b><u>Gene Function:</u></b> {$row['Gene_Function']}<br/>");
                print("<b><u>Gene Length:</u></b> {$row['Gene_Length']}<br/>");
                print("<br><br>");
            }
            $result->free();
        }
        else
        {
            print("There is no gene found with your current search criterion  :-  $attr = \"$q\" <br> Please recheck your searching criteria! <br\> <br> Thanks! <br/>");
        }

        print("</td>
    </tr>

</table> ");

$mysqli->close();

?>
