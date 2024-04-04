param(
    [switch]$Build,
    [switch]$Host_
)

Set-Location "frontend/"

if ($Build) {
    npm run build
} elseif ($Host_) {
    npm run dev -- --host
} else {
    npm run dev
}

Set-Location ".."