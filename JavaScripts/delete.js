CMS.Models.SECTION.findAll().then(function() {
  zz = can.map(CMS.Models.SECTION.cache, function(o, k) { if (/auto|Auto/.test(o.title)) return k; });

  if (zz != 0) {
    can.each(
        can.map(
            CMS.Models.SECTION.cache,
            function(o, k) {
                if (/auto|Auto/.test(o.title))
                    return k;
            }
        ).slice(0, 30),
        function(id) { CMS.Models.SECTION.cache[id].refresh().then(function(){ CMS.Models.SECTION.cache[id].destroy(); })});
}
})

