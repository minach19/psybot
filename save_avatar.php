<?php
// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Function to set CORS headers
function setCorsHeaders() {
    if (isset($_SERVER['HTTP_ORIGIN'])) {
        header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
    } else {
        header("Access-Control-Allow-Origin: http://localhost:5000");
    }
    header('Access-Control-Allow-Credentials: true');
    header('Access-Control-Max-Age: 86400');    // cache for 1 day
    header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
}

// Set CORS headers
setCorsHeaders();

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    // Return early for preflight requests
    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD'])) {
        header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    }
    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS'])) {
        header("Access-Control-Allow-Headers: {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
    }
    exit(0);
}

// Set content type for all responses
header('Content-Type: application/json; charset=UTF-8');

// Log incoming request details for debugging
error_log("Request Method: " . $_SERVER['REQUEST_METHOD']);
error_log("Request Headers: " . json_encode(getallheaders()));
error_log("Request Body: " . file_get_contents('php://input'));

// Generate a unique user ID if not exists
if (!isset($_COOKIE['user_id'])) {
    $user_id = uniqid('user_', true);
    setcookie('user_id', $user_id, time() + (86400 * 30), "/"); // 30 days
} else {
    $user_id = $_COOKIE['user_id'];
}

// Process POST request
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    
    if ($data === null) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON data']);
        exit();
    }
    
    // Save avatar configuration
    $config_file = "avatars/{$user_id}_config.json";
    if (!is_dir('avatars')) {
        mkdir('avatars', 0777, true);
    }
    
    if (file_put_contents($config_file, json_encode($data))) {
        echo json_encode(['success' => true, 'message' => 'Avatar configuration saved']);
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'Failed to save avatar configuration']);
    }
}

// Process GET request
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $config_file = "avatars/{$user_id}_config.json";
    
    if (file_exists($config_file)) {
        $config = json_decode(file_get_contents($config_file), true);
        echo json_encode($config);
    } else {
        http_response_code(404);
        echo json_encode(['error' => 'Avatar configuration not found']);
    }
}
?>
