<?php
  // Check cached data.
  $cached = file_get_contents('s.txt');
  list($threes, $threes_attempted, $games, $next) = explode(',', $cached);

  // Is there a live game?
  $live = file_get_contents('l.txt');

  if (!$live) {
    // Return cached data
    $to_json = array('threes'=>$threes,'threes_attempted'=>$threes_attempted,'games'=>$games,'next'=>$next);
  } else {
    // Get data from source.
    $contents = file_get_contents('http://sports.yahoo.com/nba/players/4612/');
    $live_contents = file_get_contents($live);

    $to_json = array('update'=>'1','contents'=>$contents,'live'=>$live,'live_contents'=>$live_contents);
  }

  echo json_encode($to_json);
?>