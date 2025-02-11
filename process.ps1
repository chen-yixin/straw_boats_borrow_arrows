# 定义输入文件路径和输出CSV文件路径
$inputFiles = Get-ChildItem -Path ".\logs" -Filter "fakessh*.log"
$outputCsv = ".\outputs\fakessh.csv"

# 初始化一个数组来存储结果
$results = @()

# 遍历每个文件
foreach ($file in $inputFiles) {
    Write-Host "Processing: $file"

    # 读取文件内容
    $lines = Get-Content -Path $file.FullName -Encoding UTF8

    # 处理每一行
    foreach ($line in $lines) {
        # 使用正则表达式分割行，确保第4个字段可以包含空格
        if ($line -match '^([\d\/]+\s[\d:\.]+)\s([\d\.]+):(\d+)\s?(.*?)\s?(\S*)\s?(\S*)$') {
            $results += [PSCustomObject]@{
                Datetime = $matches[1]
                IP = $matches[2]
                Port = $matches[3]
                Client = $matches[4]
                Username = $matches[5]
                Password = $matches[6]
            }
        }
    }
}

# 将结果导出到CSV文件
$results | Export-Csv -Path $outputCsv -NoTypeInformation -Encoding UTF8

Write-Host "Complete, output:$outputCsv"
