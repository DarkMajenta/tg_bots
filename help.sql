$rezerv = 0;
$result = $bd->query("SELECT * FROM money_box ORDER BY id DESC");
while ($row = $result->fetch_assoc()) {
    $rezerv += $row['summa'];
}

echo $rezerv; // Вывод общей суммы
