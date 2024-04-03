param(
    [switch]$Build
)

Set-Location "frontend/"

if ($Build) {
    npm run build
} else {
    npm run dev
}

Set-Location ".."