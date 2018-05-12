using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Rotator : MonoBehaviour {

	public Text resOutput;
	public Text ruleDiscription;

	// Jionts
	private GameObject[] joint;

	private int[] boneLen = { 3, 4, 5, 6,7 };

	private int curObjIndex = 1;

	private GameObject curCube;


	private Quaternion zeroRot = Quaternion.Euler (0, 0, 0);
	private Vector3 unitScale = new Vector3(1, 1, 1);
	private Vector3 zeroTran = new Vector3(0, 0, 0);

	private Matrix4x4[] boneTran;
	private Matrix4x4[] jointRot;
	private Matrix4x4 totalTransMat;

	private Vector3 cubePos;
	private Quaternion cubeQuaternion;
	private Vector3 cubeEulerAngles;

	// Use this for initialization
	void Start () {


		joint = new GameObject[5];

		joint[0] = GameObject.Find ("Joint1");
		joint[1] = GameObject.Find ("Joint2");
		joint[2] = GameObject.Find ("Joint3");
		joint[3] = GameObject.Find ("Joint4");
		joint[4] = GameObject.Find ("Joint5");

		boneTran = new Matrix4x4[4];
		jointRot = new Matrix4x4[5];
		totalTransMat = Matrix4x4.identity;

		for (int i = 0; i < 4; i++) {
			boneTran[i] = Matrix4x4.TRS (new Vector3 (0, boneLen[i], 0), zeroRot, unitScale);
		}
			
		cubePos = new Vector3 (5, 0, 0);

		curCube = GameObject.Find ("CursorCube");

		ruleDiscription.text = "Movement:" + "\n" + 
			"q: forward; " + "w: up;  " + "e: back; " + "\n" +
			"a: left;    " + "s: down;" + "d: right;" + "\n" +
			"Joint Selection: 1~5 Number" + "\n" +
			"Restoration: m";

	}
	
	// Update is called once per frame
	void Update () {

		// 1~5 select the joint
		// at the meantime record the index of current joint
		if (Input.GetKey ("1")) {
			curObjIndex = 1;
		} else if (Input.GetKey ("2")) {
			curObjIndex = 2;
		} else if (Input.GetKey ("3")) {
			curObjIndex = 3;
		} else if (Input.GetKey ("4")) {
			curObjIndex = 4;
		} else if (Input.GetKey ("5")) {
			curObjIndex = 5;
		} 
		// wsadqe control the rotations
		// while rotation, the cube also does the same rotation
		else if (Input.GetKey ("w")) {
			joint [curObjIndex - 1].transform.Rotate (Vector3.up, Space.Self);
			curCube.transform.Rotate (Vector3.up, Space.Self);
		} else if (Input.GetKey ("s")) {
			joint [curObjIndex - 1].transform.Rotate (Vector3.down, Space.Self);
			curCube.transform.Rotate (Vector3.down, Space.Self);
		} else if (Input.GetKey ("a")) {
			joint [curObjIndex - 1].transform.Rotate (Vector3.left, Space.Self);
			curCube.transform.Rotate (Vector3.left, Space.Self);
		} else if (Input.GetKey ("d")) {
			joint [curObjIndex - 1].transform.Rotate (Vector3.right, Space.Self);
			curCube.transform.Rotate (Vector3.right, Space.Self);
		} else if (Input.GetKey ("q")) {
			joint [curObjIndex - 1].transform.Rotate (Vector3.forward, Space.Self);
			curCube.transform.Rotate (Vector3.forward, Space.Self);
		} else if (Input.GetKey ("e")) {
			joint [curObjIndex - 1].transform.Rotate (Vector3.back, Space.Self);
			curCube.transform.Rotate (Vector3.back, Space.Self);
		} else if (Input.GetKey ("m")) {
			restart ();
		}

		// assign the values of position and rotation to cube after joints selection
		curCube.transform.position = joint [curObjIndex-1].transform.position;
		curCube.transform.rotation = joint [curObjIndex-1].transform.rotation;

		// computation of the total transformation matrix
		for (int i = 0; i < curObjIndex-1; i++) {
			jointRot [i].SetTRS (zeroTran, joint [i].transform.localRotation, unitScale);
			totalTransMat *= jointRot [i] * boneTran [i];
		}
		jointRot [curObjIndex-1].SetTRS (zeroTran, joint [curObjIndex-1].transform.localRotation, unitScale);
		totalTransMat *= jointRot [curObjIndex-1];

		// computation of the position of the cube
		cubePos = totalTransMat.MultiplyPoint3x4 (new Vector3 (0, 0, 0));

		// find out the quaternion and euler angles of the cube
		cubeQuaternion = Quaternion.LookRotation (totalTransMat.GetColumn (2), totalTransMat.GetColumn (1));
		cubeEulerAngles = cubeQuaternion.eulerAngles;

		// results output
		resOutput.text = "Cube Position: " + cubePos + "\n" +
			"Transform Matrix:\n" + totalTransMat + "\n" +
			"Quaternion: " + cubeQuaternion + "\n" +
			"Euler Angles: " + cubeEulerAngles;

		// restoration of the transformation matrix
		totalTransMat = Matrix4x4.identity;
	}

	void restart(){

		// restore all the rotation into (0,0,0)
//		joint [0].transform.position = new Vector3 (0, 0, 0);
		joint [0].transform.rotation = zeroRot;
		for (int i = 1; i < 5; i++) {
			joint [i].transform.rotation = zeroRot;
		}

		curCube.transform.position = new Vector3(0,0,0);
		curCube.transform.rotation = zeroRot;
		
	}
}
