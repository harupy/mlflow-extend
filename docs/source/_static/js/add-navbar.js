// Based on: https://stackoverflow.com/a/6055620
function copyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.style.position = "fixed";
  textArea.style.top = 0;
  textArea.style.left = 0;
  textArea.style.width = "2em";
  textArea.style.height = "2em";
  textArea.style.padding = 0;
  textArea.style.border = "none";
  textArea.style.outline = "none";
  textArea.style.boxShadow = "none";
  textArea.style.background = "transparent";
  textArea.value = text;

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  document.execCommand("copy");

  document.body.removeChild(textArea);
}

function removePromptsAndOutput(doctest) {
  function isCode(line) {
    return line.startsWith(">>> ") || line.startsWith("... ");
  }

  function stripPrompt(line) {
    return line.replace(">>> ", "").replace("... ", "");
  }

  return doctest.split(/\r|\n/).filter(isCode).map(stripPrompt).join("\n");
}

// Based on: https://github.com/scikit-learn/scikit-learn/blob/a7e17117bb15eb3f51ebccc1bd53e42fcb4e6cd8/doc/themes/scikit-learn/static/js/copybutton.js
$(document).ready(function () {
  var div = $(
    ".highlight-python .highlight," +
      ".highlight-python3 .highlight," +
      ".highlight-pycon .highlight," +
      ".highlight-default .highlight"
  );
  var pre = div.find("pre");

  // get the styles from the current theme
  pre.parent().parent().css("position", "relative");
  var hideText = "Hide the prompts and output";
  var showText = "Show the prompts and output";

  var navbarStyles = {
    "background-color": div.css("background-color"),
    padding: "2px 12px",
    border: " 1px solid #e1e4e5",
  };

  var buttonStyles = {
    "border-radius": "4px",
    "margin-right": "2px",
  };

  var msgStyles = {
    "margin-left": "4px",
  };

  // create and add the button to all the code blocks that contain >>>
  div.each(function (index) {
    var jthis = $(this);
    if (jthis.find(".gp").length > 0) {
      var navbar = $('<div class="navbar"></div>');
      navbar.css(navbarStyles);

      // create a copy button
      var copyButton = $('<button type="button"></button>');
      var clipboardIcon = $(
        '<img src="https://clipboardjs.com/assets/images/clippy.svg" width="13" alt="Copy to clipboard">'
      );
      copyButton.append(clipboardIcon);
      copyButton.addClass("copy-button");
      copyButton.css(buttonStyles);
      copyButton.attr("title", "Copy to clipboard");

      // create a hide button
      var hideButton = $('<button type="button">&gt;&gt;&gt;</button>'); // "&gt;&gt;&gt;" is ">>>"
      hideButton.addClass("hide-button");
      hideButton.css(buttonStyles);
      hideButton.attr("title", hideText);
      hideButton.data("hidden", "false");

      //
      var msg = $("<span>Copied!</span>");
      msg.addClass("message");
      msg.css(msgStyles);
      msg.css("visibility", "hidden");

      // place the copy and hide buttons above the doctest block
      navbar.append(copyButton);
      navbar.append(hideButton);
      navbar.append(msg);
      navbar.insertBefore(jthis);
    }
    // tracebacks (.gt) contain bare text elements that need to be
    // wrapped in a span to work with .nextUntil() (see later)
    jthis
      .find("pre:has(.gt)")
      .contents()
      .filter(function () {
        return this.nodeType == 3 && this.data.trim().length > 0;
      })
      .wrap("<span>");
  });

  // define the behavior of the copy button when it's clicked
  $(".copy-button").click(function (e) {
    e.preventDefault();
    var button = $(this);
    var div = button.parent().parent().find("div.highlight");
    var doctest = div.text();

    var hidden =
      button.parent().find("button.hide-button").data("hidden") === "true";

    // If the hide button is clicked, remove the prompts and output.
    if (hidden) {
      doctest = removePromptsAndOutput(doctest);
    }

    copyTextToClipboard(doctest);

    var msg = $("span.message");
    msg.css("visibility", "visible");
    setTimeout(function () {
      msg.css("visibility", "hidden");
    }, 1000);
  });

  // define the behavior of the hide button when it's clicked
  $(".hide-button").click(function (e) {
    e.preventDefault();
    var button = $(this);
    var div = button.parent().parent().find("div.highlight");
    if (button.data("hidden") === "false") {
      // hide the code output
      div.find(".go, .gp, .gt").hide();
      div
        .next("pre")
        .find(".gt")
        .nextUntil(".gp, .go")
        .css("visibility", "hidden");

      button.css("text-decoration", "line-through");
      button.attr("title", showText);
      button.data("hidden", "true");
    } else {
      // show the code output
      div.find(".go, .gp, .gt").show();
      div
        .next("pre")
        .find(".gt")
        .nextUntil(".gp, .go")
        .css("visibility", "visible");

      button.css("text-decoration", "none");
      button.attr("title", hideText);
      button.data("hidden", "false");
    }
  });
});
