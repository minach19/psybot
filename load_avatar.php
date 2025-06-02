<?php
// File: load_avatar.php
// This script loads the avatar configuration and image from the server using XAMPP

// --- Improved CORS Headers with dynamic origin handling ---
// Log incoming request details for debugging
$logFile = fopen("avatar_load_debug.txt", "a");
fwrite($logFile, "\n--- New Request " . date('Y-m-d H:i:s') . " ---\n");
fwrite($logFile, "REQUEST_METHOD: " . $_SERVER['REQUEST_METHOD'] . "\n");
if(isset($_SERVER['HTTP_ORIGIN'])) {
    fwrite($logFile, "HTTP_ORIGIN: " . $_SERVER['HTTP_ORIGIN'] . "\n");
}
fwrite($logFile, "REQUEST_URI: " . $_SERVER['REQUEST_URI'] . "\n");
fwrite($logFile, "REMOTE_ADDR: " . $_SERVER['REMOTE_ADDR'] . "\n");
fclose($logFile);

// Get the origin from the request
$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';

// List of allowed origins - add more as needed
$allowed_origins = array(
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    'http://localhost',
    'http://127.0.0.1',
    'null'  // For local file access
);

// Set the CORS headers based on origin
if (in_array($origin, $allowed_origins)) {
    header("Access-Control-Allow-Origin: $origin");
} else {
    // If origin is not in allowed list, use wildcard (less secure but more permissive)
    header("Access-Control-Allow-Origin: *");
}

// Enable preflight caching
header("Access-Control-Max-Age: 86400");
// These headers are needed for preflight requests
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
// If your requests include credentials (cookies, auth headers)
header("Access-Control-Allow-Credentials: true");

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

header("Content-Type: application/json; charset=UTF-8");

// Function to get user ID from cookie
function getUserId() {
    if (isset($_COOKIE['psybot_user_id'])) {
        return $_COOKIE['psybot_user_id'];
    }
    return null;
}

// Directory to store avatar data
$avatar_dir = __DIR__ . '/uploads/avatars/';

// Get the user ID from cookie or request parameter
$user_id = isset($_GET['user_id']) ? $_GET['user_id'] : getUserId();

if (!$user_id) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'No user ID provided']);
    exit;
}

// Check if configuration file exists
$config_file = $avatar_dir . $user_id . '_config.json';
if (!file_exists($config_file)) {
    http_response_code(404);
    echo json_encode(['status' => 'error', 'message' => 'Avatar configuration not found']);
    exit;
}

// Read configuration
$avatar_config = json_decode(file_get_contents($config_file), true);

// Check if image exists
$image_file = $avatar_dir . $user_id . '_avatar.png';
$image_url = '';
if (file_exists($image_file)) {
    $image_url = 'uploads/avatars/' . $user_id . '_avatar.png';
}

// Return data
echo json_encode([
    'status' => 'success',
    'user_id' => $user_id,
    'avatar_config' => $avatar_config,
    'image_url' => $image_url
]);
?>
