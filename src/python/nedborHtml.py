#import modules.myutils as myutils
import modules.nedborUtils as nbu
import sys

language = sys.argv[1] if len(sys.argv)>1 else 'None'

csvPath = "../../data/"
nedborutil = nbu.NedborUtil(csvPath)
nedborutil.saveAllNedborData(lang=language,type="html")
nedborutil.saveAllNedborData(lang="None")
nedborutil.saveAllNedborData(lang="da")

df = nedborutil.nedborToDataframe()

flip = False
if flip:
    newdf = df.transpose()    
    nedborutil.makeHtml("../../public/",newdf, True)
else:
    nedborutil.makeHtml("../../public/",df, False)

print("Done")