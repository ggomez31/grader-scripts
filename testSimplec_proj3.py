import os
import sys
import glob 
import shutil 
import subprocess 
from lib import cd, Submission, run_cmd

source_path = os.path.dirname(os.path.abspath(__file__)) # /a/b/c/d/e
test_case_points = 0.875
build_points = 1 #points for building. tentative


def buildAndTest(submissionpath, sourceTestPath):
    

    points = 0
    script_path = os.path.dirname(os.path.realpath(__file__))

    # create temporary directory so that previous students' results will not affect subsequent tests
    testCasePath = sourceTestPath

    testCases = glob.glob(os.path.join(testCasePath, "*.simplec"))
    #print(f"testCases {testCases}")

    for i in glob.glob(os.path.join(submissionpath, "*.o")):
        if os.path.exists(i):
            os.remove(i)
    progname = os.path.join(submissionpath, "simplec")
    if os.path.exists(progname):
        os.remove(progname)

    if len(testCases) == 0:
        print("# no tests found.  double-check your path: " + testCasePath)
        sys.exit()


    if os.path.exists(submissionpath + "/simplec"):
        os.remove(submissionpath + "/simplec")
    print("# building your simplec compiler")
    out = subprocess.run(['make'], cwd = submissionpath,
            stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

    output = ""
    err = ""
    if out.returncode != 0:
        output += "Make failed. Skipping test cases and exiting.\n"  
        print(output + " Do you have a Makefile?") # can't even compile the compiler 
        return 0, output 
    else:
        print("Build succeeded")
        output += "Build succeeded\n"
        points += build_points # points to build. tentative   
    
    # simpleC compilers lives so lets go through every test case now
    for case in testCases:
        base_name = os.path.basename(case)
        print(f"Testing {base_name}:", end=" ")

        with cd(submissionpath):
            ground_truth = case.replace(".simplec", ".s")
            cmd = f"cat \"{case}\" | ./simplec > {base_name}.out"
            #print(f"Running command: {cmd}")
            return_code, stdout_, stderr_ = run_cmd(cmd)
            cmd = f"diff -w -B \"{ground_truth}\" {base_name}.out"
            #print(f"Running command: {cmd}")
            return_code, stdout_, stderr_ = run_cmd(cmd,False)
            if return_code == 0 and len(stdout_) == 0:
                print("Success!")
                output += f"{base_name}: pass\n"
                points += test_case_points
            if return_code == 1 and len(stdout_) > 0:
                print(f"Failure. See {base_name}.diff for diff and {base_name}.out for output.")
                output += f"{base_name}: fail. See {base_name}.diff for diff and {base_name}.out for output.\n"
                cmd = f"diff -w -B \"{ground_truth}\" {base_name}.out > {base_name}.diff"
                return_code, stdout_, stderr_ = run_cmd(cmd)
            if return_code > 1:
                print(f"diff exited with an unknown return code. This shouldn't happen. Here is the stderr: {stderr_}")
    msg = f"{int((points - build_points) / test_case_points)} / {len(testCases)} test casing passing."
    print(msg)
    output += msg
    return points, output 

def error(app, f):

    return "# ERROR " + app + " failed on " + f + "\n"
    

if __name__ == "__main__":

    try:
        submissionDirectory = os.path.abspath(sys.argv[1])
        sourceTestPath = os.path.abspath(sys.argv[2])
    except:
        print("USAGE: path/to/your/repo path/to/the/tests")
        print("example: ./ ../syllabus/projects/tests/proj0/")
        sys.exit()


    buildAndTest(submissionDirectory, sourceTestPath)
    #os.remove()