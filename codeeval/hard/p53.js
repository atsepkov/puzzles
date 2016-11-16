function sortSuffixes(line) {
    var suffixes = new Array(line.length);
    var length = line.length;
    for (var i = 0; i < length; i++) {
        suffixes[i] = i;
    }
    suffixes.sort(function(a, b) {
        if (line.substring(a) < line.substring(b)) return -1;
        if (line.substring(a) > line.substring(b)) return 1;
        return 0;
    });
    return suffixes;
}

function findLongestCommonPrefix(a, b, length) {
    var i = 0;
    while (i < length && a.charAt(i) === b.charAt(i)) i++;
    return i;
}

var fs = require("fs");
fs.readFileSync(process.argv[2]).toString().split('\n').forEach(function (line) {
    if (line !== "") {
        console.log(">", line);
        suffixArray = sortSuffixes(line);
        var one = line.substring(suffixArray[0]);
        var i = 1, length = suffixArray.length;
        var longestPrefix = 0, longestIndex = NaN;
//        console.log(suffixArray.map(function(e) {
//            return "  " + e + " |" + line.substring(e);
//        }));
        while (i < length) {
            var two = line.substring(suffixArray[i]);
            if (one.trim().length) {
                var currentPrefix = findLongestCommonPrefix(one, two, Math.min(
                    one.length,
                    Math.abs(suffixArray[i-1] - suffixArray[i])
                ));
                if (
                    (currentPrefix > longestPrefix || currentPrefix === longestPrefix &&
                    (suffixArray[i] < longestIndex || suffixArray[i-1] < longestIndex)) &&
                    line.substring(suffixArray[i], suffixArray[i] + currentPrefix).trim().length
                ) {
                    longestPrefix = currentPrefix;
                    longestIndex = suffixArray[i];
                }
            }
            
            i++;
            one = two;
        }
        
        if (isNaN(longestIndex)) {
            console.log("NONE");
        } else {
            console.log("|" + line.substring(longestIndex, longestIndex + longestPrefix) + "|");
        }
    }
});
