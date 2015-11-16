<?php

// Accept threes, games, and next game. Concat with modtime.
$file = 'data/s.txt';
$updated_threes = $_POST['t'];
$updated_threes_attempted = $_POST['ta'];
$updated_games = $_POST['g'];
$updated_next_game = $_POST['ng'];

$cached = file_get_contents($file);
list($threes, $threes_attempted, $games, $next, $update_time) = explode(',', $cached);

// Only update if 3pm, 3pa, or games is incremented
if ($updated_threes > $threes || $updated_threes_attempted > $threes_attempted || $updated_games > $games) {
  $str = $updated_threes . ',' . $updated_threes_attempted . ',' . $updated_games . ',' . $updated_next_game;

  // Save text to file.
  file_put_contents($file, $str);

  // Generate new img by hitting the generate stats url.
  $curl = curl_init('http://' . $_SERVER['HTTP_HOST'] . '/generate_stat_card.php');
  $result = curl_exec($curl);
}

?>