window.sc3s = {
  _record: 286,

  _tCacheKey: 'sc3s:t',
  _taCacheKey: 'sc3s:ta',
  _gCacheKey: 'sc3s:g',
  _ngCacheKey: 'sc3s:ng',
  _lCacheKey: 'sc3s:l',

  _ms: {
    'January': '1',
    'February': '2',
    'March': '3',
    'April': '4',
    'May': '5',
    'June': '6',
    'July': '7',
    'August': '8',
    'September': '9',
    'October': '10',
    'November': '11',
    'December': '12',
  },

  _data: {
    threes: null,
    games: null,
    nextGame: null,
    live: null,
  },

  init: function() {
    this._preloadFromCache();
    this._startPoll();

    $(window).on('resize', this._onResize.bind(this));
  },

  _startPoll: function() {
    this._getData();
    setInterval(this._getData.bind(this), 30000);
  },

  _updateUI: function() {
    // Return if no threes or games info.
    // Page can still function without game indicator.
    if (!this._data.threes || !this._data.games) return;

    var pace = Math.floor((this._data.threes/this._data.games)*82);

    $('#pace > span:first-child').html(pace);
    $('#threes > span:first-child').html(this._data.threes);
    $('#games > span:first-child').html(this._data.games);
    $('#pct > span:first-child').html(this._data.pct);

    // UI adjustments for higher numbers.
    // Hack for justify shortcomings.
    $('#3ptrs-label').html(parseInt(this._data.threes) > 99 ? '3PTRS' : '3 PTRS');

    if (this._data.live) {
      $('#l').show();
      $('#nl').hide();
    } else {
      $('#ng').html(this._data.nextGame);
      $('#nl').show();
      $('#l').hide();
    }

    this._updateGraph();
  },

  _getData: function() {
    $.get('data/stats.php', this._onData.bind(this));
  },

  _setCached: function(key, val) {
    if (typeof(Storage) == "undefined") return;
    return window.localStorage.setItem(key, val);
  },

  _getCached: function(key) {
    if (typeof(Storage) == "undefined") return;
    return window.localStorage.getItem(key);
  },

  _preloadFromCache: function() {
    this._data.threes = this._getCached(this._tCacheKey);
    this._data.threesAttempted = this._getCached(this._taCacheKey);
    this._data.games = this._getCached(this._gCacheKey);
    this._data.nextGame = this._getCached(this._ngCacheKey);
    this._data.live = this._getCached(this._lCacheKey);
    this._data.pct = this._computePct();

    this._updateUI();
  },

  _onServerCachedData: function(data) {
    this._setLocalCache(data.threes, data.threes_attempted, data.games, data.next);
    this._updateUI();
  },

  _computePct: function(threes, attempted) {
    // Default to cached.
    var threes = threes || this._data.threes;
    var attempted = attempted || this._data.threesAttempted;

    if (!threes || !attempted) return;

    var threes = parseInt(this._data.threes);
    var attempted = parseInt(this._data.threesAttempted);
    return parseFloat((threes/attempted)*100).toFixed(1);
  },

  _onData: function(r) {
    r = JSON.parse(r);

    if (!r['update']) return this._onServerCachedData(r);

    var $statsDoc = $(r['contents']);
    var $liveDoc = $(r['live_contents']);
    var live = r['live'];
    var monthAndDate = $statsDoc.find('.yom-sports-player-next-game .list .date h3').html().split(' ');
    var nextGame = this._ms[monthAndDate[1]] + '/' + monthAndDate[2];

    // Scrape player page.
    var threes = $statsDoc.find('[summary="Player Season Totals"] th:contains("2015-16")').parent().find('.3-point-shots-made').html();
    var threesAttempted = $statsDoc.find('[summary="Player Season Totals"] th:contains("2015-16")').parent().find('.3-point-shots-attemped').html();
    var games = $statsDoc.find('[summary="Player Season Totals"] th:contains("2015-16")').parent().find('.games').html();

    if (live) {
      var $playerEntry = $liveDoc.find('th#table-1-nba\\.p\\.4612');

      if ($playerEntry.length) {
        var tDelta = parseInt($playerEntry.parent().find('.three-pointers').html().split('-')[0]);
        var taDelta = parseInt($playerEntry.parent().find('.three-pointers').html().split('-')[1]);
        threes = parseInt(threes) + tDelta;
        threesAttempted = parseInt(threesAttempted) + taDelta;
        games = parseInt(games) + 1;
      } else {
        live = undefined;
      }
    }

    // Cache locally and on server.
    this._setLocalCache(threes, threesAttempted, games, nextGame, live);
    $.post('u.php', { t: threes, ta: threesAttempted, g: games, ng: nextGame });

    this._updateUI();
  },

  _onResize: function(e) {
	// Add filters to bg image if width is mobile or less.
	var windowWidth = $(e.currentTarget).width();
	$('#sc-img1, #sc-img2').toggleClass('filter', windowWidth <= 450);
	this._updateGraph(e);
  },

  _updateGraph: function(e) {
    var $img = $('#sc-img1').is(':visible') ? $('#sc-img1') : null;

    // Reset heights first if this was the result of a resize.
    if (e) {
      $('#r-mtr, #curr').removeClass('transition');
      $('#r-mtr, #curr').height(0);
    }

    // Update current total on the graph.
    $('#curr-indctr .t-num').html(this._data.threes);

    // Now update the graph bar.
    $('#r-mtr, #curr').addClass('transition');
    $('#r-mtr').height($img ? $img.height() + 'px' : '100%');
    $('#curr').height((this._data.threes/this._record)*100 + '%');
  },

  // Set local data object and local storage entry.
  _setLocalCache: function(t, ta, g, ng, l) {
    this._data.threes = t;
    this._data.threesAttempted = ta;
    this._data.games = g;
    this._data.nextGame = ng;
    this._data.live = l;
    this._data.pct = this._computePct();

    this._setCached(this._tCacheKey, t);
    this._setCached(this._taCacheKey, ta);
    this._setCached(this._gCacheKey, g);
    this._setCached(this._ngCacheKey, ng);

    if (!l) return window.localStorage.removeItem(this._lCacheKey);

    this._setCached(this._lCacheKey, l);
  },

  cp: function(key) {
    key = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
    var match = location.search.match(new RegExp("[?&]"+key+"=([^&]+)(&|$)"));

    if (!match) {
      window.location = 'http://scthrees.com';
    }

    var p = decodeURIComponent(match[1].replace(/\+/g, " "))

    if (p != 'asdf78901234jkl') {
      window.location = window.location.origin;
    }
  },
};