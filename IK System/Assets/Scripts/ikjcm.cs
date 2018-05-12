using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

public class ikjcm : MonoBehaviour {

	public GameObject joint1;
	public GameObject joint2;
	public GameObject basejoint;

	private Vector3 bone1_length;
	private Vector3 bone2_length;

	float bone_length;

	public GameObject cursor;

	bool reach_target = true;
	float[] theta = new float[2];

	public Text instruction;
	string message;


	// Use this for initialization
	void Start () {

		joint1 = GameObject.Find ("joint1");
		joint2 = GameObject.Find ("joint2");
		basejoint = GameObject.Find ("basejoint");

		bone1_length = GameObject.Find ("bone1").transform.lossyScale;
		bone2_length = GameObject.Find ("bone2").transform.lossyScale;

		bone_length = bone1_length.y + bone2_length.y;

		cursor = GameObject.Find ("cursor");

		message = "Movement:" + "\n" + 
			"↑: up   ↓: down   \n" + 
			"←: left   →: right   \n" +
			"i: go get target   \n" +
			"target: ";

		instruction.text = message + "reaching";
		
	}
	
	// Update is called once per frame
	void Update () {

		cursorControl ();
		ik ();
		
	}

	void cursorControl(){

		if (Input.GetKey (KeyCode.UpArrow)) {
			cursor.transform.position += new Vector3 (0, 0.1f, 0);
			instruction.text = message + "reaching";
		} else if (Input.GetKey (KeyCode.DownArrow)) {
			cursor.transform.position += new Vector3 (0, -0.1f, 0);
			instruction.text = message + "reaching";
		} else if (Input.GetKey (KeyCode.LeftArrow)) {
			cursor.transform.position += new Vector3 (-0.1f, 0, 0);
			instruction.text = message + "reaching";
		} else if (Input.GetKey (KeyCode.RightArrow)) {
			cursor.transform.position += new Vector3 (0.1f, 0, 0);
			instruction.text = message + "reaching";
		} else if (Input.GetKeyDown (KeyCode.I)) {
			instruction.text = message + "reaching";
			reach_target = false;
			findTheta ();
		}
	}

	void ik(){

		if (!reach_target) {

			// distance between target(cursor) and E(end-effector)
			float d1 = Mathf.Sqrt (distanceSq (cursor.transform.position - joint2.transform.position));
			// distance between target(cursor) and base joint
			float d2 = Mathf.Sqrt (distanceSq (cursor.transform.position - basejoint.transform.position)) - bone_length;
			
            // two situation of being reached target:
			// 1. overlap
			// 2. out of reach but closest
			// p.s. 1.01 and 0.01 are used for precision tolerance
			if (d2 > 0 && d1 < d2 * 1.01f || d1 < 0.01) {
				reach_target = true;
				instruction.text = message + "reached";
			} else {
				// constant 0.1f used in base joint in case rotating too fast
				basejoint.transform.Rotate (new Vector3 (0, 0, 0.1f * theta [0]));
				// did not use constant because theta[1] was usually too small
				joint1.transform.Rotate (new Vector3 (0, 0,  theta [1]));
				// recalculate the theta after every rotation to be of high precision
				findTheta ();
			}
		}

	}

	void findTheta(){

		Vector3 V = cursor.transform.position - joint2.transform.position;

		Vector3 E = joint2.transform.position;
		Vector3 P1 = joint1.transform.position;

		Vector3 J_col1 = crossProduct (new Vector3(0,0,1), E);
		Vector3 J_col2 = crossProduct (new Vector3(0,0,1), (E - P1));

		float[,] J = new float[,]{ { J_col1.x, J_col2.x }, { J_col1.y, J_col2.y }, { J_col1.z, J_col2.z } };

		float[,] JT = matrixTranspose (J);

		//	======I tried to use pseudoinverse matrix to compute J, however it didn't perform well===========
//		float[,] JTJ = matricesProduct (JT, J);
//		float[,] JTJinverse = matrix2X2Inverse (JTJ);
//		float[,] Jp;
//		if (JTJinverse == null) {
//			Jp = JT;
//		} else {
//			Jp = matricesProduct (JTJinverse, JT);
//		}
		// ================================================================================================

		theta [0] = theta [1] = 0; 
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < 3; j++) {
				theta [i] += JT [i, j] * V [j];
			}
		}
	}

	Vector3 crossProduct(Vector3 v1, Vector3 v2){
		return new Vector3 (
			v1.y * v2.z - v1.z * v2.y,
			v1.z * v2.x - v1.x * v2.z,
			v1.x * v2.y - v1.y * v2.x
		);
	}

	float distanceSq(Vector3 v){
		return v.x * v.x + v.y * v.y + v.z * v.z;
	}

	float[,] matrixTranspose(float[,] m){
		int r = m.GetLength (0);
		int c = m.GetLength (1);
		float[,] res = new float[c, r];
		for (int i = 0; i < c; i++) {
			for (int j = 0; j < r; j++) {
				res [i, j] = m [j, i];
			}
		}

		return res;
	}

    //	========= I tried to use pseudoinverse matrix to compute J, however it didn't perform well =============
	//  ========= The following functions were used for sudoinverse matrix computation =======================
	float[,] matrix2X2Inverse(float[,] m){

		float delta = m [0, 0] * m [1, 1] - m [0, 1] * m [1, 0];
		if (delta == 0)
			return null;
		float[,] res = new float[2, 2]{ { m [1, 1], (-1) * m [0, 1] }, { (-1) * m [1, 0], m [0, 0] } };
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < 2; j++) {
				res [i, j] = 1 / delta * m [i, j]; 
			}
		}
		return res;
	}

	float[,] matricesProduct(float[,] m1, float[,] m2){
		int lenRow1 = m1.GetLength (0);
		int lenCol1 = m1.GetLength (1);
		int lenRow2 = m2.GetLength (0);
		int lenCol2 = m2.GetLength (1);

		if (lenCol1 != lenRow2)
			return null;

		float[,] res = new float[lenRow1, lenCol2];
		for (int i = 0; i < lenRow1; i++) {
			for (int j = 0; j < lenCol2; j++) {
				for (int k = 0; k < lenCol1; k++) {
					res [i, j] += m1 [i, k] * m2 [k, j]; 
				}
			}
		}
		return res;
	}

}







