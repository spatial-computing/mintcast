./bin/mintcast.sh -t netcdf --structure "{year}/FLDAS_NOAH01_C_EA_M.A{year}{month}.001.nc" -s '201701' --end-time "201801" --dir /Users/liber/Documents/hydro1.gesdisc.eosdis.nasa.gov/data/FLDAS/FLDAS_NOAH01_C_EA_M.001 -z "{year}/FLDAS_NOAH01_C_EA_M.A{year}{month}.001.nc/*.mbtiles" -m aef24c836d5dea24a8196e077d1367bf --single-subdataset Rainf_f_tavg -o FLDAS_NOAH01_C_EA_M.A2017 --datatime-format "{year}{month}" --with-shape-file "./shp/WBD.shp" --load-colormap "./shp/ylgnbl_colormap.txt" -l FLDAS_C_Rainf_f_tavg_2017_Monthly --dev-mode-off --tile-server-root "./" --scp-to-default-server --verbose

# FLDAS_NOAH01_C_EA_M.A201710.001